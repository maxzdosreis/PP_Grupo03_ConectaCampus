from datetime import timedelta

import pytest
from django.core.cache import cache
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone
from redis.exceptions import RedisError

from reservas.api import dependencias
from reservas.infrastructure.indice_redis import IndiceDeReservasRedis

pytestmark = pytest.mark.django_db

URL_FILA = reverse("reservas:pendentes")
URL_CONTAGEM = reverse("reservas:contagem_por_situacao")
SITUACOES = ["SOLICITADA", "CONFIRMADA", "RECUSADA", "CANCELADA", "CONCLUIDA"]


def _amanha():
    return timezone.localdate() + timedelta(days=1)


def _solicitar(cliente, espaco_id, hora):
    return cliente.post(
        reverse("reservas:lista"),
        {
            "espaco_id": espaco_id,
            "data": _amanha().isoformat(),
            "hora_inicio": f"{hora:02d}:00",
            "hora_fim": f"{hora + 1:02d}:00",
            "finalidade": "Treino de vôlei",
        },
        format="json",
    ).data["dados"]["id"]


def _alterar(cliente, reserva_id, corpo):
    return cliente.patch(
        reverse("reservas:situacao", args=[reserva_id]), corpo, format="json"
    )


def _montar_o_indice():
    dependencias.reconstruir_indice().executar()
    assert IndiceDeReservasRedis().pendentes(1) is not None


def _apagar_o_sinal_do_indice():
    chave = cache.make_key("reservas:indice:montado")
    cache._cache.get_client(chave, write=True).delete(chave)
    assert IndiceDeReservasRedis().pendentes(1) is None


def _quebrar_o_redis(monkeypatch):
    def cliente_fora_do_ar(*args, **kwargs):
        raise RedisError("Redis fora do ar")

    monkeypatch.setattr(
        "reservas.infrastructure.indice_redis.cliente", cliente_fora_do_ar
    )


@pytest.fixture
def tres_pendentes(cliente_solicitante, cliente_gestor, espaco_id):
    tarde = _solicitar(cliente_solicitante, espaco_id, 15)
    cedo = _solicitar(cliente_solicitante, espaco_id, 9)
    confirmada = _solicitar(cliente_solicitante, espaco_id, 12)
    assert _alterar(cliente_gestor, confirmada, {"situacao": "CONFIRMADA"}).status_code
    pendente = _solicitar(cliente_solicitante, espaco_id, 18)
    return {"ordem": [tarde, cedo, pendente], "confirmada": confirmada}


def _resumo(resposta):
    corpo = resposta.json()
    return corpo["mensagem"], corpo["dados"], corpo.get("paginacao")


@pytest.mark.parametrize("url", [URL_FILA, URL_CONTAGEM])
def test_anonimo_recebe_401(client, url):
    resposta = client.get(url)

    assert resposta.status_code == 401
    assert resposta.json()["erro"]["codigo"] == "NAO_AUTENTICADO"


@pytest.mark.parametrize("url", [URL_FILA, URL_CONTAGEM])
def test_solicitante_recebe_403_mesmo_com_reservas_proprias(
    cliente_solicitante, tres_pendentes, url
):
    resposta = cliente_solicitante.get(url)

    assert resposta.status_code == 403
    assert resposta.json()["erro"]["codigo"] == "ACAO_NAO_PERMITIDA"


@pytest.mark.parametrize("url", [URL_FILA, URL_CONTAGEM])
@pytest.mark.parametrize("metodo", ["post", "put", "patch", "delete"])
def test_outros_metodos_recebem_405(cliente_gestor, url, metodo):
    resposta = getattr(cliente_gestor, metodo)(url)

    assert resposta.status_code == 405
    assert resposta.json()["erro"]["codigo"] == "METODO_NAO_PERMITIDO"


@pytest.mark.parametrize(
    ("consulta", "campo"),
    [
        ({"pagina": "0"}, "pagina"),
        ({"pagina": "abc"}, "pagina"),
        ({"tamanho": "101"}, "tamanho"),
        ({"tamanho": "0"}, "tamanho"),
    ],
)
def test_parametro_invalido_recebe_400_com_o_campo(cliente_gestor, consulta, campo):
    resposta = cliente_gestor.get(URL_FILA, consulta)

    assert resposta.status_code == 400
    erro = resposta.json()["erro"]
    assert erro["codigo"] == "DADOS_INVALIDOS"
    assert campo in erro["campos"]


def test_solicitante_com_parametro_invalido_recebe_403_e_nao_400(cliente_solicitante):
    resposta = cliente_solicitante.get(URL_FILA, {"pagina": "0"})

    assert resposta.status_code == 403


def test_fila_vem_em_ordem_de_solicitacao_com_o_formato_da_reserva(
    cliente_gestor, tres_pendentes
):
    # Arrange
    _montar_o_indice()

    # Act
    resposta = cliente_gestor.get(URL_FILA)

    # Assert
    corpo = resposta.json()
    assert resposta.status_code == 200
    assert corpo["mensagem"] == "3 reservas pendentes."
    assert [r["id"] for r in corpo["dados"]] == tres_pendentes["ordem"]
    assert {r["situacao"] for r in corpo["dados"]} == {"SOLICITADA"}
    assert {"solicitante", "hora_inicio", "criada_em", "acoes_disponiveis"} <= set(
        corpo["dados"][0]
    )
    assert corpo["paginacao"] == {
        "pagina": 1,
        "tamanho": 20,
        "total": 3,
        "total_de_paginas": 1,
    }


def test_fila_vazia_diz_que_nao_ha_pendentes(cliente_gestor):
    resposta = cliente_gestor.get(URL_FILA)

    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Nenhuma reserva pendente."
    assert resposta.json()["dados"] == []


def test_fila_com_uma_reserva_usa_o_singular(
    cliente_gestor, cliente_solicitante, espaco_id
):
    _solicitar(cliente_solicitante, espaco_id, 10)

    resposta = cliente_gestor.get(URL_FILA)

    assert resposta.json()["mensagem"] == "1 reserva pendente."


def test_fila_pagina_e_depois_da_ultima_vem_vazia_com_o_total(
    cliente_gestor, tres_pendentes
):
    # Arrange
    _montar_o_indice()

    # Act
    segunda = cliente_gestor.get(URL_FILA, {"pagina": 2, "tamanho": 2})
    alem = cliente_gestor.get(URL_FILA, {"pagina": 3, "tamanho": 2})

    # Assert
    assert [r["id"] for r in segunda.json()["dados"]] == tres_pendentes["ordem"][2:]
    assert alem.json()["dados"] == []
    assert alem.json()["paginacao"]["total"] == 3
    assert alem.json()["paginacao"]["total_de_paginas"] == 2


def test_contagem_traz_as_cinco_situacoes_na_ordem_com_zeros(
    cliente_gestor, tres_pendentes
):
    # Arrange
    _montar_o_indice()

    # Act
    resposta = cliente_gestor.get(URL_CONTAGEM)

    # Assert
    dados = resposta.json()["dados"]
    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Contagem das reservas por situação."
    assert [s["situacao"] for s in dados["situacoes"]] == SITUACOES
    assert [s["total"] for s in dados["situacoes"]] == [3, 1, 0, 0, 0]
    assert dados["situacoes"][0]["rotulo"] == "Solicitada"
    assert dados["total"] == 4


def test_contagem_sem_reservas_traz_tudo_zerado(cliente_gestor):
    dados = cliente_gestor.get(URL_CONTAGEM).json()["dados"]

    assert [s["total"] for s in dados["situacoes"]] == [0, 0, 0, 0, 0]
    assert dados["total"] == 0


def test_resposta_com_a_projecao_montada_e_a_do_banco_sao_iguais(
    cliente_gestor, tres_pendentes
):
    # Arrange
    _montar_o_indice()

    # Act
    fila_do_indice = _resumo(cliente_gestor.get(URL_FILA, {"tamanho": 2}))
    contagem_do_indice = _resumo(cliente_gestor.get(URL_CONTAGEM))
    _apagar_o_sinal_do_indice()
    fila_do_banco = _resumo(cliente_gestor.get(URL_FILA, {"tamanho": 2}))
    contagem_do_banco = _resumo(cliente_gestor.get(URL_CONTAGEM))

    # Assert
    assert fila_do_indice == fila_do_banco
    assert contagem_do_indice == contagem_do_banco


def test_resposta_com_a_projecao_fora_do_ar_e_a_mesma_e_nunca_503(
    cliente_gestor, tres_pendentes, monkeypatch
):
    # Arrange
    _montar_o_indice()
    fila_esperada = _resumo(cliente_gestor.get(URL_FILA))
    contagem_esperada = _resumo(cliente_gestor.get(URL_CONTAGEM))
    _quebrar_o_redis(monkeypatch)

    # Act
    fila = cliente_gestor.get(URL_FILA)
    contagem = cliente_gestor.get(URL_CONTAGEM)

    # Assert
    assert fila.status_code == contagem.status_code == 200
    assert _resumo(fila) == fila_esperada
    assert _resumo(contagem) == contagem_esperada


def test_projecao_atrasada_nao_mostra_reserva_que_ja_saiu_de_solicitada(
    cliente_gestor, tres_pendentes
):
    # Arrange
    _montar_o_indice()
    from reservas.infrastructure.models import ReservaModel

    ReservaModel.objects.filter(pk=tres_pendentes["ordem"][0]).update(
        situacao="CONFIRMADA"
    )

    # Act
    resposta = cliente_gestor.get(URL_FILA)

    # Assert
    assert [r["id"] for r in resposta.json()["dados"]] == tres_pendentes["ordem"][1:]
    assert resposta.json()["paginacao"]["total"] == 2


def test_confirmar_pela_api_tira_da_fila_e_muda_a_contagem_sem_reconstruir(
    cliente_gestor, tres_pendentes, django_capture_on_commit_callbacks
):
    # Arrange
    _montar_o_indice()
    alvo = tres_pendentes["ordem"][0]

    # Act
    with django_capture_on_commit_callbacks(execute=True):
        resposta = _alterar(cliente_gestor, alvo, {"situacao": "CONFIRMADA"})
    fila = cliente_gestor.get(URL_FILA)
    contagem = cliente_gestor.get(URL_CONTAGEM)

    # Assert
    assert resposta.status_code == 200
    assert [r["id"] for r in fila.json()["dados"]] == tres_pendentes["ordem"][1:]
    assert fila.json()["paginacao"]["total"] == 2
    totais = [s["total"] for s in contagem.json()["dados"]["situacoes"]]
    assert totais == [2, 2, 0, 0, 0]


def test_nova_solicitacao_entra_no_fim_da_fila_sem_reconstruir(
    cliente_gestor,
    cliente_solicitante,
    espaco_id,
    tres_pendentes,
    django_capture_on_commit_callbacks,
):
    # Arrange
    _montar_o_indice()

    # Act
    with django_capture_on_commit_callbacks(execute=True):
        nova = _solicitar(cliente_solicitante, espaco_id, 20)
    fila = cliente_gestor.get(URL_FILA)

    # Assert
    assert [r["id"] for r in fila.json()["dados"]] == [*tres_pendentes["ordem"], nova]


def _consultas_de_reservas(consultas):
    return [c["sql"] for c in consultas if "reservas_reserva" in c["sql"]]


def test_contagem_com_a_projecao_montada_nao_consulta_a_tabela_de_reservas(
    cliente_gestor, tres_pendentes
):
    # Arrange
    _montar_o_indice()

    # Act
    with CaptureQueriesContext(connection) as consultas:
        resposta = cliente_gestor.get(URL_CONTAGEM)

    # Assert
    assert resposta.status_code == 200
    assert _consultas_de_reservas(consultas) == []


def test_fila_com_a_projecao_montada_so_le_as_reservas_da_pagina_por_id(
    cliente_gestor, tres_pendentes
):
    # Arrange
    _montar_o_indice()

    # Act
    with CaptureQueriesContext(connection) as consultas:
        resposta = cliente_gestor.get(URL_FILA)

    # Assert
    assert resposta.status_code == 200
    lidas = _consultas_de_reservas(consultas)
    assert len(lidas) == 1
    assert "COUNT" not in lidas[0]
    assert " IN (" in lidas[0]


def test_sem_projecao_a_contagem_faz_um_group_by_e_a_fila_faz_count_e_limit(
    cliente_gestor, tres_pendentes
):
    # Act
    with CaptureQueriesContext(connection) as da_contagem:
        cliente_gestor.get(URL_CONTAGEM)
    with CaptureQueriesContext(connection) as da_fila:
        cliente_gestor.get(URL_FILA)

    # Assert
    assert any("GROUP BY" in sql for sql in _consultas_de_reservas(da_contagem))
    sqls = _consultas_de_reservas(da_fila)
    assert any("COUNT" in sql for sql in sqls)
    assert any("LIMIT" in sql for sql in sqls)


def test_ler_a_fila_nao_repovoa_a_projecao(cliente_gestor, tres_pendentes):
    # Arrange
    assert IndiceDeReservasRedis().pendentes(1) is None

    # Act
    cliente_gestor.get(URL_FILA)
    cliente_gestor.get(URL_CONTAGEM)

    # Assert
    assert IndiceDeReservasRedis().pendentes(1) is None
    assert IndiceDeReservasRedis().contagem_por_situacao() is None
