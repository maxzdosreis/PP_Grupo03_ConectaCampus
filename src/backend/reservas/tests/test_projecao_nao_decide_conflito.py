from datetime import time, timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from reservas.api import dependencias
from reservas.application.ocupacao_do_dia import HorarioOcupado
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.agenda_redis import AgendaDoDiaRedis
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango
from reservas.tests.fakes import ANA, FUNCIONAMENTO_PADRAO, intervalo
from reservas.tests.redis_de_teste import (
    ocupados_do_postgres,
    ocupados_do_redis,
    projetar_dia,
    redis_limpo_depois,  # noqa: F401
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("redis_limpo_depois"),
]

ID_FANTASMA = 999_999


def _amanha():
    return timezone.localdate() + timedelta(days=1)


def _guardar_no_postgres(espaco_id):
    reserva = Reserva.solicitar(
        espaco_id=espaco_id,
        solicitante=ANA,
        data=_amanha(),
        hora_inicio=time(10, 0),
        hora_fim=time(11, 0),
        finalidade="Treino do time",
        agora=timezone.now(),
        funcionamento=FUNCIONAMENTO_PADRAO,
    )
    return RepositorioReservasDjango().salvar(reserva)


def _solicitar(cliente, espaco_id):
    return cliente.post(
        reverse("reservas:lista"),
        {
            "espaco_id": espaco_id,
            "data": _amanha().isoformat(),
            "hora_inicio": "10:00",
            "hora_fim": "11:00",
            "finalidade": "Treino de vôlei",
        },
        format="json",
    )


def _ocupacao(cliente, espaco_id):
    resposta = cliente.get(
        reverse("reservas:ocupacao"),
        {"espaco": espaco_id, "data": _amanha().isoformat()},
    )
    assert resposta.status_code == 200
    return resposta.data["dados"]["ocupados"]


def test_projecao_que_diz_livre_nao_impede_o_conflito_e_a_reconstrucao_a_corrige(
    cliente_solicitante, espaco_id, django_capture_on_commit_callbacks
):
    # DEC-28 (a) em ação: a projeção errada não decide, o PostgreSQL decide.
    # Arrange
    _guardar_no_postgres(espaco_id)
    projetar_dia(espaco_id, _amanha())
    assert ocupados_do_redis(espaco_id, _amanha()) == []

    # Act
    with django_capture_on_commit_callbacks(execute=True):
        resposta = _solicitar(cliente_solicitante, espaco_id)
    lido_da_projecao = _ocupacao(cliente_solicitante, espaco_id)
    dependencias.reconstruir_agenda().executar()
    lido_depois = _ocupacao(cliente_solicitante, espaco_id)

    # Assert
    assert resposta.status_code == 409
    assert resposta.data["erro"]["codigo"] == "CONFLITO_DE_HORARIO"
    assert lido_da_projecao == []
    assert len(lido_depois) == 1
    assert ocupados_do_redis(espaco_id, _amanha()) == ocupados_do_postgres(
        espaco_id, _amanha()
    )


def test_projecao_que_diz_ocupado_nao_impede_a_reserva_e_a_reconstrucao_a_corrige(
    cliente_solicitante, espaco_id, django_capture_on_commit_callbacks
):
    # DEC-28 (a) em ação: um horário "ocupado" só na projeção não bloqueia ninguém.
    # Arrange
    agenda = AgendaDoDiaRedis()
    fantasma = HorarioOcupado(
        intervalo=intervalo("10:00", "11:00", _amanha()),
        situacao=SituacaoReserva.CONFIRMADA,
    )
    versao = agenda.versao(espaco_id, _amanha())
    assert agenda.substituir(
        espaco_id, _amanha(), {ID_FANTASMA: fantasma}, versao=versao
    )
    assert ocupados_do_postgres(espaco_id, _amanha()) == []

    # Act
    antes = _ocupacao(cliente_solicitante, espaco_id)
    with django_capture_on_commit_callbacks(execute=True):
        resposta = _solicitar(cliente_solicitante, espaco_id)
    com_o_fantasma = _ocupacao(cliente_solicitante, espaco_id)
    dependencias.reconstruir_agenda().executar()
    depois = _ocupacao(cliente_solicitante, espaco_id)

    # Assert
    assert [o["situacao"] for o in antes] == ["CONFIRMADA"]
    assert resposta.status_code == 201
    assert sorted(o["situacao"] for o in com_o_fantasma) == ["CONFIRMADA", "SOLICITADA"]
    assert [o["situacao"] for o in depois] == ["SOLICITADA"]
    assert ocupados_do_redis(espaco_id, _amanha()) == ocupados_do_postgres(
        espaco_id, _amanha()
    )
