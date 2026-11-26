from datetime import timedelta

import pytest
from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone
from redis.exceptions import RedisError

from reservas.api import dependencias
from reservas.infrastructure.ranking_redis import RankingDeEspacosRedis

pytestmark = pytest.mark.django_db

URL = reverse("reservas:ranking_de_espacos")


@pytest.fixture(autouse=True)
def _projecoes_na_hora(monkeypatch):
    """Sem transação real no teste, o on_commit nunca roda: executa na hora."""
    monkeypatch.setattr(
        "reservas.infrastructure.repositorio_com_agenda.transaction.on_commit",
        lambda acao, **opcoes: acao(),
    )


def _amanha():
    return timezone.localdate() + timedelta(days=1)


def _novo_espaco(cliente_gestor, nome):
    resposta = cliente_gestor.post(
        reverse("espacos:lista"),
        {"nome": nome, "tipo": "GINASIO", "capacidade": 30},
        format="json",
    )
    return resposta.data["dados"]["id"]


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


def _confirmar(cliente_solicitante, cliente_gestor, espaco_id, hora):
    reserva_id = _solicitar(cliente_solicitante, espaco_id, hora)
    assert (
        _alterar(cliente_gestor, reserva_id, {"situacao": "CONFIRMADA"}).status_code
        == 200
    )
    return reserva_id


def _montar_o_ranking():
    dependencias.reconstruir_ranking().executar()
    assert RankingDeEspacosRedis().top(1) is not None


def _apagar_o_sinal_do_ranking():
    chave = cache.make_key("ranking:montado")
    cache._cache.get_client(chave, write=True).delete(chave)
    assert RankingDeEspacosRedis().top(1) is None


def _quebrar_o_redis(monkeypatch):
    def cliente_fora_do_ar(*args, **kwargs):
        raise RedisError("Redis fora do ar")

    monkeypatch.setattr(
        "reservas.infrastructure.ranking_redis.cliente", cliente_fora_do_ar
    )


def _resumo(resposta):
    corpo = resposta.json()
    return corpo["mensagem"], corpo["dados"]


@pytest.fixture
def tres_espacos(cliente_gestor, cliente_solicitante):
    central = _novo_espaco(cliente_gestor, "Quadra Central")
    norte = _novo_espaco(cliente_gestor, "Campo Norte")
    sul = _novo_espaco(cliente_gestor, "Ginásio Sul")
    _confirmar(cliente_solicitante, cliente_gestor, central, 8)
    _confirmar(cliente_solicitante, cliente_gestor, central, 10)
    _confirmar(cliente_solicitante, cliente_gestor, norte, 9)
    _solicitar(cliente_solicitante, sul, 11)
    return {"central": central, "norte": norte, "sul": sul}


def test_anonimo_recebe_401(client):
    resposta = client.get(URL)

    assert resposta.status_code == 401
    assert resposta.json()["erro"]["codigo"] == "NAO_AUTENTICADO"


def test_solicitante_recebe_403_mesmo_com_reservas_confirmadas(
    cliente_solicitante, tres_espacos
):
    resposta = cliente_solicitante.get(URL)

    assert resposta.status_code == 403
    assert resposta.json()["erro"]["codigo"] == "ACAO_NAO_PERMITIDA"


@pytest.mark.parametrize("metodo", ["post", "put", "patch", "delete"])
def test_outros_metodos_recebem_405(cliente_gestor, metodo):
    resposta = getattr(cliente_gestor, metodo)(URL)

    assert resposta.status_code == 405
    assert resposta.json()["erro"]["codigo"] == "METODO_NAO_PERMITIDO"


@pytest.mark.parametrize("limite", ["0", "-1", "21", "abc", "1.5"])
def test_limite_invalido_recebe_400_com_o_campo(cliente_gestor, limite):
    resposta = cliente_gestor.get(URL, {"limite": limite})

    assert resposta.status_code == 400
    erro = resposta.json()["erro"]
    assert erro["codigo"] == "DADOS_INVALIDOS"
    assert "limite" in erro["campos"]


def test_solicitante_com_limite_invalido_recebe_403_e_nao_400(cliente_solicitante):
    resposta = cliente_solicitante.get(URL, {"limite": "0"})

    assert resposta.status_code == 403


@pytest.mark.parametrize("limite", ["1", "20"])
def test_limites_nas_bordas_sao_aceitos(cliente_gestor, limite):
    assert cliente_gestor.get(URL, {"limite": limite}).status_code == 200


def test_sem_reservas_confirmadas_diz_que_nao_ha_ranking(cliente_gestor):
    resposta = cliente_gestor.get(URL)

    assert resposta.status_code == 200
    assert _resumo(resposta) == ("Nenhuma reserva confirmada ainda.", [])


def test_ranking_vem_em_ordem_com_posicao_nome_e_total(cliente_gestor, tres_espacos):
    # Act
    resposta = cliente_gestor.get(URL)

    # Assert
    assert resposta.status_code == 200
    assert _resumo(resposta) == (
        "2 espaços no ranking.",
        [
            {
                "posicao": 1,
                "espaco_id": tres_espacos["central"],
                "nome": "Quadra Central",
                "total": 2,
            },
            {
                "posicao": 2,
                "espaco_id": tres_espacos["norte"],
                "nome": "Campo Norte",
                "total": 1,
            },
        ],
    )


def test_ranking_com_um_espaco_usa_o_singular(
    cliente_gestor, cliente_solicitante, espaco_id
):
    # Arrange
    _confirmar(cliente_solicitante, cliente_gestor, espaco_id, 8)

    # Act
    mensagem, dados = _resumo(cliente_gestor.get(URL))

    # Assert
    assert mensagem == "1 espaço no ranking."
    assert dados == [
        {"posicao": 1, "espaco_id": espaco_id, "nome": "Quadra Coberta", "total": 1}
    ]


def test_limite_corta_a_lista_e_o_padrao_e_cinco(cliente_gestor, cliente_solicitante):
    # Arrange
    espacos = [_novo_espaco(cliente_gestor, f"Quadra {i}") for i in range(6)]
    for espaco in espacos:
        _confirmar(cliente_solicitante, cliente_gestor, espaco, 8)

    # Act
    padrao = cliente_gestor.get(URL).json()["dados"]
    um = cliente_gestor.get(URL, {"limite": 1}).json()["dados"]

    # Assert
    assert [p["espaco_id"] for p in padrao] == espacos[:5]
    assert [p["posicao"] for p in padrao] == [1, 2, 3, 4, 5]
    assert [p["espaco_id"] for p in um] == espacos[:1]


def test_espaco_desativado_continua_no_ranking_com_o_nome(
    cliente_gestor, cliente_solicitante, espaco_id
):
    # Arrange
    _confirmar(cliente_solicitante, cliente_gestor, espaco_id, 8)
    desativar = reverse("espacos:desativar", args=[espaco_id])
    assert cliente_gestor.post(desativar).status_code == 200

    # Act
    _, dados = _resumo(cliente_gestor.get(URL))

    # Assert
    assert [(p["nome"], p["total"]) for p in dados] == [("Quadra Coberta", 1)]


def test_resposta_com_o_ranking_montado_e_a_do_banco_sao_iguais(
    cliente_gestor, tres_espacos
):
    # Arrange
    _montar_o_ranking()

    # Act
    do_ranking = _resumo(cliente_gestor.get(URL, {"limite": 2}))
    _apagar_o_sinal_do_ranking()
    do_banco = _resumo(cliente_gestor.get(URL, {"limite": 2}))

    # Assert
    assert do_ranking == do_banco
    assert len(do_banco[1]) == 2


def test_resposta_com_o_redis_fora_do_ar_e_a_mesma_e_nunca_503(
    cliente_gestor, tres_espacos, monkeypatch
):
    # Arrange
    _montar_o_ranking()
    esperada = _resumo(cliente_gestor.get(URL))
    _quebrar_o_redis(monkeypatch)

    # Act
    resposta = cliente_gestor.get(URL)

    # Assert
    assert resposta.status_code == 200
    assert _resumo(resposta) == esperada


def test_confirmar_pela_api_muda_o_ranking_sem_reconstruir(
    cliente_gestor, cliente_solicitante, tres_espacos
):
    # Arrange
    _montar_o_ranking()
    pendente = _solicitar(cliente_solicitante, tres_espacos["sul"], 13)
    assert len(cliente_gestor.get(URL).json()["dados"]) == 2

    # Act
    assert (
        _alterar(cliente_gestor, pendente, {"situacao": "CONFIRMADA"}).status_code
        == 200
    )

    # Assert
    posicoes = cliente_gestor.get(URL).json()["dados"]
    assert [(p["espaco_id"], p["total"]) for p in posicoes] == [
        (tres_espacos["central"], 2),
        (tres_espacos["norte"], 1),
        (tres_espacos["sul"], 1),
    ]


def test_cancelar_uma_confirmada_pela_api_tira_do_ranking_sem_reconstruir(
    cliente_gestor, cliente_solicitante, tres_espacos
):
    # Arrange
    do_norte = _confirmar(
        cliente_solicitante, cliente_gestor, tres_espacos["norte"], 15
    )
    _montar_o_ranking()
    antes = cliente_gestor.get(URL).json()["dados"]
    assert [p["total"] for p in antes] == [2, 2]

    # Act
    corpo = {"situacao": "CANCELADA", "motivo": "Chuva forte"}
    assert _alterar(cliente_gestor, do_norte, corpo).status_code == 200

    # Assert
    depois = cliente_gestor.get(URL).json()["dados"]
    assert [(p["espaco_id"], p["total"]) for p in depois] == [
        (tres_espacos["central"], 2),
        (tres_espacos["norte"], 1),
    ]


def test_cancelar_a_unica_confirmada_do_espaco_o_tira_do_ranking(
    cliente_gestor, cliente_solicitante, espaco_id
):
    # Arrange
    reserva_id = _confirmar(cliente_solicitante, cliente_gestor, espaco_id, 8)
    _montar_o_ranking()
    assert len(cliente_gestor.get(URL).json()["dados"]) == 1

    # Act
    corpo = {"situacao": "CANCELADA", "motivo": "Chuva forte"}
    assert _alterar(cliente_gestor, reserva_id, corpo).status_code == 200

    # Assert
    assert _resumo(cliente_gestor.get(URL)) == ("Nenhuma reserva confirmada ainda.", [])


def test_repetir_o_mesmo_pedido_nao_conta_duas_vezes(
    cliente_gestor, cliente_solicitante, espaco_id
):
    # Arrange
    _montar_o_ranking()
    reserva_id = _solicitar(cliente_solicitante, espaco_id, 8)

    # Act
    primeira = _alterar(cliente_gestor, reserva_id, {"situacao": "CONFIRMADA"})
    segunda = _alterar(cliente_gestor, reserva_id, {"situacao": "CONFIRMADA"})

    # Assert
    assert primeira.status_code == 200
    assert segunda.status_code == 409
    assert [p["total"] for p in cliente_gestor.get(URL).json()["dados"]] == [1]


def test_ler_o_ranking_nao_repovoa_a_projecao(cliente_gestor, tres_espacos):
    # Act
    cliente_gestor.get(URL)

    # Assert
    assert RankingDeEspacosRedis().top(5) is None
