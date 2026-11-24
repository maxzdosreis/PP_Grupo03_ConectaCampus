from datetime import timedelta

import pytest
from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone
from redis.exceptions import RedisError

from reservas.infrastructure.agenda_redis import AgendaDoDiaRedis
from reservas.infrastructure.repositorio_com_agenda import (
    RepositorioReservasComAgenda,
)
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango
from reservas.tests.fakes import DIA, reserva_solicitada

pytestmark = pytest.mark.django_db

URL_RESERVAS = reverse("reservas:lista")
ESPACO_AVULSO = 77


def _amanha():
    return timezone.localdate() + timedelta(days=1)


def _chave(espaco_id, data):
    return cache.make_key(f"agenda:espaco:{espaco_id}:{data.isoformat()}")


def _chave_da_versao(espaco_id, data):
    return cache.make_key(f"agenda:versao:espaco:{espaco_id}:{data.isoformat()}")


def _membros(espaco_id, data):
    chave = _chave(espaco_id, data)
    bruto = cache._cache.get_client(chave, write=False).zrange(chave, 0, -1)
    textos = (m.decode() if isinstance(m, bytes) else m for m in bruto)
    return sorted(texto for texto in textos if texto != "_")


def _versao(espaco_id, data):
    return AgendaDoDiaRedis().versao(espaco_id, data)


def _criar_projecao(espaco_id, data):
    agenda = AgendaDoDiaRedis()
    versao = agenda.versao(espaco_id, data)
    assert agenda.substituir(espaco_id, data, {}, versao=versao)


def _solicitar(cliente, espaco_id):
    return cliente.post(
        URL_RESERVAS,
        {
            "espaco_id": espaco_id,
            "data": _amanha().isoformat(),
            "hora_inicio": "10:00",
            "hora_fim": "11:00",
            "finalidade": "Treino de vôlei",
        },
        format="json",
    )


def _alterar(cliente, reserva_id, corpo):
    url = reverse("reservas:situacao", args=[reserva_id])
    return cliente.patch(url, corpo, format="json")


def _quebrar_o_redis(monkeypatch):
    def cliente_fora_do_ar(*args, **kwargs):
        raise RedisError("Redis fora do ar")

    monkeypatch.setattr(
        "reservas.infrastructure.agenda_redis._cliente", cliente_fora_do_ar
    )


def test_solicitar_reserva_coloca_o_membro_na_agenda_do_dia(
    cliente_solicitante, espaco_id, django_capture_on_commit_callbacks
):
    # Arrange
    _criar_projecao(espaco_id, _amanha())

    # Act
    with django_capture_on_commit_callbacks(execute=True):
        resposta = _solicitar(cliente_solicitante, espaco_id)

    # Assert
    assert resposta.status_code == 201
    reserva_id = resposta.data["dados"]["id"]
    assert _membros(espaco_id, _amanha()) == [f"{reserva_id}:660:SOLICITADA"]
    assert _chave(espaco_id, _amanha()).startswith("conecta-campus:1:agenda:espaco:")


def test_confirmar_troca_o_membro_e_cancelar_remove(
    cliente_solicitante, cliente_gestor, espaco_id, django_capture_on_commit_callbacks
):
    # Arrange
    _criar_projecao(espaco_id, _amanha())
    with django_capture_on_commit_callbacks(execute=True):
        reserva_id = _solicitar(cliente_solicitante, espaco_id).data["dados"]["id"]

    # Act
    with django_capture_on_commit_callbacks(execute=True):
        confirmada = _alterar(cliente_gestor, reserva_id, {"situacao": "CONFIRMADA"})
    depois_de_confirmar = _membros(espaco_id, _amanha())
    with django_capture_on_commit_callbacks(execute=True):
        cancelada = _alterar(
            cliente_gestor,
            reserva_id,
            {"situacao": "CANCELADA", "motivo": "Quadra interditada"},
        )

    # Assert
    assert confirmada.status_code == 200
    assert depois_de_confirmar == [f"{reserva_id}:660:CONFIRMADA"]
    assert cancelada.status_code == 200
    assert _membros(espaco_id, _amanha()) == []


def test_sem_projecao_do_dia_nada_e_gravado_mas_a_versao_avanca(
    cliente_solicitante, espaco_id, django_capture_on_commit_callbacks
):
    # Arrange
    antes = _versao(espaco_id, _amanha())

    # Act
    with django_capture_on_commit_callbacks(execute=True):
        resposta = _solicitar(cliente_solicitante, espaco_id)

    # Assert
    assert resposta.status_code == 201
    assert _membros(espaco_id, _amanha()) == []
    assert _versao(espaco_id, _amanha()) == antes + 1


def test_rollback_da_transacao_de_fora_nao_chega_ao_redis(
    django_capture_on_commit_callbacks,
):
    # Arrange
    _criar_projecao(ESPACO_AVULSO, DIA)
    repositorio = RepositorioReservasComAgenda(
        RepositorioReservasDjango(), AgendaDoDiaRedis()
    )

    def salvar_e_falhar():
        with repositorio.em_transacao():
            repositorio.salvar(reserva_solicitada(espaco_id=ESPACO_AVULSO))
            raise RuntimeError("erro depois do salvar")

    # Act
    with (
        django_capture_on_commit_callbacks(execute=True) as callbacks,
        pytest.raises(RuntimeError),
    ):
        salvar_e_falhar()

    # Assert
    assert callbacks == []
    assert _membros(ESPACO_AVULSO, DIA) == []
    assert (
        RepositorioReservasDjango().listar_que_ocupam_horario(ESPACO_AVULSO, DIA) == []
    )


def test_dentro_de_em_transacao_a_agenda_so_muda_no_commit_de_fora(
    django_capture_on_commit_callbacks,
):
    # Arrange
    _criar_projecao(ESPACO_AVULSO, DIA)
    repositorio = RepositorioReservasComAgenda(
        RepositorioReservasDjango(), AgendaDoDiaRedis()
    )

    def salvar_e_olhar_o_redis():
        with repositorio.em_transacao():
            salva = repositorio.salvar(reserva_solicitada(espaco_id=ESPACO_AVULSO))
            return salva, _membros(ESPACO_AVULSO, DIA)

    # Act
    with django_capture_on_commit_callbacks(execute=True) as callbacks:
        salva, durante = salvar_e_olhar_o_redis()

    # Assert
    assert durante == []
    assert len(callbacks) == 1
    assert _membros(ESPACO_AVULSO, DIA) == [f"{salva.id}:660:SOLICITADA"]


@pytest.mark.django_db(transaction=True)
def test_sem_transacao_aberta_a_agenda_e_atualizada_na_hora():
    # Arrange
    _criar_projecao(ESPACO_AVULSO, DIA)
    repositorio = RepositorioReservasComAgenda(
        RepositorioReservasDjango(), AgendaDoDiaRedis()
    )

    # Act
    salva = repositorio.salvar(reserva_solicitada(espaco_id=ESPACO_AVULSO))

    # Assert
    assert _membros(ESPACO_AVULSO, DIA) == [f"{salva.id}:660:SOLICITADA"]


def test_redis_fora_do_ar_na_criacao_nao_derruba_a_reserva(
    cliente_solicitante, espaco_id, monkeypatch, django_capture_on_commit_callbacks
):
    # Arrange
    _quebrar_o_redis(monkeypatch)

    # Act
    with django_capture_on_commit_callbacks(execute=True):
        resposta = _solicitar(cliente_solicitante, espaco_id)

    # Assert
    assert resposta.status_code == 201
    reserva_id = resposta.data["dados"]["id"]
    assert RepositorioReservasDjango().obter_por_id(reserva_id) is not None


def test_redis_fora_do_ar_na_mudanca_de_situacao_nao_derruba_a_alteracao(
    cliente_solicitante,
    cliente_gestor,
    espaco_id,
    monkeypatch,
    django_capture_on_commit_callbacks,
):
    # Arrange
    reserva_id = _solicitar(cliente_solicitante, espaco_id).data["dados"]["id"]
    _quebrar_o_redis(monkeypatch)

    # Act
    with django_capture_on_commit_callbacks(execute=True):
        resposta = _alterar(cliente_gestor, reserva_id, {"situacao": "CONFIRMADA"})

    # Assert
    assert resposta.status_code == 200
    gravada = RepositorioReservasDjango().obter_por_id(reserva_id)
    assert gravada.situacao.value == "CONFIRMADA"
