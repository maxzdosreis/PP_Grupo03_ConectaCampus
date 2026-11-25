from datetime import timedelta

import pytest
from django.core.cache import cache
from django.db import connection, transaction
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone
from redis.exceptions import RedisError

from compartilhado.infrastructure.redis_comum import cliente
from espacos import publico
from espacos.infrastructure import cache_de_espacos_redis

pytestmark = pytest.mark.django_db

URL_RESERVAS = reverse("reservas:lista")
URL_OCUPACAO = reverse("reservas:ocupacao")


def _detalhe(espaco_id):
    return reverse("espacos:detalhe", args=[espaco_id])


def _chave(espaco_id):
    return cache.make_key(f"espaco:{espaco_id}")


def _amanha():
    return timezone.localdate() + timedelta(days=1)


def _consultas_a(tabela, funcao):
    with CaptureQueriesContext(connection) as capturadas:
        resposta = funcao()
    return resposta, [q for q in capturadas if tabela in q["sql"]]


def _ocupacao(cliente_http, espaco_id):
    return cliente_http.get(
        URL_OCUPACAO, {"espaco": espaco_id, "data": _amanha().isoformat()}
    )


def _solicitar(cliente_http, espaco_id, inicio, fim):
    return cliente_http.post(
        URL_RESERVAS,
        {
            "espaco_id": espaco_id,
            "data": _amanha().isoformat(),
            "hora_inicio": inicio,
            "hora_fim": fim,
            "finalidade": "Treino do time",
        },
        format="json",
    )


def _envenenar(espaco_id, **campos):
    dados = {
        "nome": "Quadra Coberta",
        "tipo": "QUADRA_POLIESPORTIVA",
        "capacidade": "20",
        "ativo": "1",
        "abertura_em_minutos": "0",
        "fechamento_em_minutos": "1440",
    }
    dados.update({k: str(v) for k, v in campos.items()})
    cliente(_chave(espaco_id), escrita=True).hset(_chave(espaco_id), mapping=dados)


def test_segundo_get_do_espaco_nao_consulta_a_tabela_de_espacos(
    cliente_solicitante, espaco_id
):
    # Arrange
    primeira, _ = _consultas_a(
        "espacos_espaco_esportivo", lambda: cliente_solicitante.get(_detalhe(espaco_id))
    )

    # Act
    segunda, consultas = _consultas_a(
        "espacos_espaco_esportivo", lambda: cliente_solicitante.get(_detalhe(espaco_id))
    )

    # Assert
    assert primeira.status_code == segunda.status_code == 200
    assert segunda.data == primeira.data
    assert consultas == []
    assert cliente(_chave(espaco_id), escrita=False).ttl(_chave(espaco_id)) > 0


def test_ocupacao_com_agenda_e_espaco_em_cache_nao_consulta_reservas_nem_espacos(
    cliente_solicitante, espaco_id
):
    # Arrange
    _ocupacao(cliente_solicitante, espaco_id)

    # Act
    resposta, consultas = _consultas_a(
        "espaco", lambda: _ocupacao(cliente_solicitante, espaco_id)
    )
    _, de_reservas = _consultas_a(
        "reservas_reserva", lambda: _ocupacao(cliente_solicitante, espaco_id)
    )

    # Assert
    assert resposta.status_code == 200
    assert consultas == []
    assert de_reservas == []


def test_editar_apaga_a_chave_e_o_get_seguinte_traz_o_dado_novo(
    cliente_gestor, cliente_solicitante, espaco_id, django_capture_on_commit_callbacks
):
    # Arrange
    cliente_solicitante.get(_detalhe(espaco_id))
    assert cliente(_chave(espaco_id), escrita=False).exists(_chave(espaco_id)) == 1

    # Act
    with django_capture_on_commit_callbacks(execute=True):
        editou = cliente_gestor.patch(
            _detalhe(espaco_id), {"nome": "Quadra Renomeada"}, format="json"
        )

    # Assert
    assert editou.status_code == 200
    assert cliente(_chave(espaco_id), escrita=False).exists(_chave(espaco_id)) == 0
    assert cliente_solicitante.get(_detalhe(espaco_id)).data["dados"]["nome"] == (
        "Quadra Renomeada"
    )


def test_desativar_bloqueia_a_ocupacao_na_hora_e_reativar_volta_a_200(
    cliente_gestor, cliente_solicitante, espaco_id, django_capture_on_commit_callbacks
):
    # Arrange
    assert _ocupacao(cliente_solicitante, espaco_id).status_code == 200

    # Act
    with django_capture_on_commit_callbacks(execute=True):
        cliente_gestor.post(reverse("espacos:desativar", args=[espaco_id]))
    inativo = _ocupacao(cliente_solicitante, espaco_id)
    with django_capture_on_commit_callbacks(execute=True):
        cliente_gestor.post(reverse("espacos:ativar", args=[espaco_id]))
    ativo = _ocupacao(cliente_solicitante, espaco_id)

    # Assert
    assert inativo.status_code == 409
    assert inativo.data["erro"]["codigo"] == "ESPACO_INATIVO"
    assert ativo.status_code == 200


def test_cache_envenenado_com_horario_largo_nao_vence_o_horario_real_na_decisao(
    cliente_gestor,
    cliente_solicitante,
    espaco_id,
    django_capture_on_commit_callbacks,
):
    # Arrange
    with django_capture_on_commit_callbacks(execute=True):
        cliente_gestor.patch(
            _detalhe(espaco_id), {"fechamento": "22:00"}, format="json"
        )
    _envenenar(espaco_id)

    # Act
    informativa = _ocupacao(cliente_solicitante, espaco_id)
    decisao = _solicitar(cliente_solicitante, espaco_id, "23:00", "23:30")

    # Assert
    assert informativa.data["dados"]["horario_de_fechamento"] == "00:00"
    assert decisao.status_code == 400
    assert decisao.data["erro"]["codigo"] == "FORA_DO_HORARIO_DE_FUNCIONAMENTO"


def test_cache_envenenado_dizendo_inativo_nao_impede_reservar_espaco_ativo(
    cliente_solicitante, espaco_id
):
    # Arrange
    _envenenar(espaco_id, ativo=0)

    # Act
    informativa = _ocupacao(cliente_solicitante, espaco_id)
    decisao = _solicitar(cliente_solicitante, espaco_id, "10:00", "11:00")

    # Assert
    assert informativa.status_code == 409
    assert decisao.status_code == 201


def test_a_validacao_para_reservar_ignora_o_cache_envenenado(espaco_id):
    # Arrange
    _envenenar(espaco_id, ativo=0, fechamento_em_minutos=600)

    # Act
    with transaction.atomic():
        decisao = publico.verificar_espaco_disponivel_para_reserva(espaco_id)
    informativa = publico.verificar_espaco_disponivel

    # Assert
    assert decisao.fechamento_em_minutos == 1440
    with pytest.raises(Exception, match="inativo"):
        informativa(espaco_id)


def test_redis_fora_do_ar_as_leituras_seguem_200_com_o_dado_do_postgres(
    cliente_solicitante, espaco_id, monkeypatch
):
    # Arrange
    def cliente_que_falha(chave, *, escrita):
        raise RedisError("fora do ar")

    monkeypatch.setattr(cache_de_espacos_redis, "cliente", cliente_que_falha)

    # Act
    detalhe = cliente_solicitante.get(_detalhe(espaco_id))
    ocupacao = _ocupacao(cliente_solicitante, espaco_id)

    # Assert
    assert detalhe.status_code == 200
    assert detalhe.data["dados"]["nome"] == "Quadra Coberta"
    assert ocupacao.status_code == 200


def test_hash_com_tipo_errado_nao_derruba_a_leitura(cliente_solicitante, espaco_id):
    # Arrange
    cliente(_chave(espaco_id), escrita=True).set(_chave(espaco_id), "lixo")

    # Act
    resposta = cliente_solicitante.get(_detalhe(espaco_id))

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"]["nome"] == "Quadra Coberta"


def test_invalidacao_com_redis_fora_do_ar_nao_desfaz_a_edicao(
    cliente_gestor,
    cliente_solicitante,
    espaco_id,
    monkeypatch,
    django_capture_on_commit_callbacks,
):
    # Arrange
    def cliente_que_falha(chave, *, escrita):
        raise RedisError("fora do ar")

    monkeypatch.setattr(cache_de_espacos_redis, "cliente", cliente_que_falha)

    # Act
    with django_capture_on_commit_callbacks(execute=True):
        editou = cliente_gestor.patch(
            _detalhe(espaco_id), {"nome": "Nome Novo"}, format="json"
        )
    monkeypatch.undo()

    # Assert
    assert editou.status_code == 200
    assert cliente_solicitante.get(_detalhe(espaco_id)).data["dados"]["nome"] == (
        "Nome Novo"
    )
