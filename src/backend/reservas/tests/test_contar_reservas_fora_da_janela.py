from datetime import datetime

import pytest

from reservas.application.casos_de_uso import ContarReservasAtivasForaDaJanela
from reservas.domain.intervalo_de_horario import FUSO_HORARIO
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import (
    AGORA,
    DIA,
    RepositorioReservasEmMemoria,
    intervalo,
    reserva_reconstituida,
)

S = SituacaoReserva
MINUTOS_07H = 7 * 60
MINUTOS_22H = 22 * 60
MINUTOS_NO_DIA = 24 * 60


@pytest.fixture
def repositorio():
    return RepositorioReservasEmMemoria()


@pytest.fixture
def contar(repositorio):
    return ContarReservasAtivasForaDaJanela(repositorio, lambda: AGORA)


def _salvar(repositorio, situacao, inicio, fim, *, espaco_id=3, data=DIA):
    return repositorio.salvar(
        reserva_reconstituida(
            id=None,
            espaco_id=espaco_id,
            intervalo=intervalo(inicio, fim, data),
            situacao=situacao,
        )
    )


def test_sem_reservas_nao_ha_nenhuma_fora_da_janela(contar):
    # Act / Assert
    assert contar.executar(3, MINUTOS_07H, MINUTOS_22H) == 0


def test_conta_so_as_que_nao_cabem_inteiras_na_nova_janela(repositorio, contar):
    # Arrange
    _salvar(repositorio, S.SOLICITADA, "10:00", "11:00")
    _salvar(repositorio, S.CONFIRMADA, "21:30", "22:30")
    _salvar(repositorio, S.SOLICITADA, "23:00", "00:00")
    _salvar(repositorio, S.CONFIRMADA, "06:00", "07:00")

    # Act
    fora = contar.executar(3, MINUTOS_07H, MINUTOS_22H)

    # Assert
    assert fora == 3


def test_reserva_que_termina_exatamente_no_fechamento_cabe(repositorio, contar):
    # Arrange
    _salvar(repositorio, S.SOLICITADA, "21:00", "22:00")
    _salvar(repositorio, S.SOLICITADA, "07:00", "08:00")

    # Act / Assert
    assert contar.executar(3, MINUTOS_07H, MINUTOS_22H) == 0


def test_reserva_ate_a_meia_noite_cabe_so_se_o_fechamento_for_a_meia_noite(
    repositorio, contar
):
    # Arrange
    _salvar(repositorio, S.CONFIRMADA, "23:00", "00:00")

    # Act / Assert
    assert contar.executar(3, MINUTOS_07H, MINUTOS_NO_DIA) == 0
    assert contar.executar(3, MINUTOS_07H, MINUTOS_NO_DIA - 1) == 1


def test_so_conta_reservas_ativas_do_espaco_e_ainda_nao_terminadas(repositorio):
    # Arrange
    cancelada = reserva_reconstituida(
        id=None,
        espaco_id=3,
        intervalo=intervalo("21:30", "22:30"),
        situacao=S.CANCELADA,
    )
    repositorio.salvar(cancelada)
    _salvar(repositorio, S.SOLICITADA, "21:30", "22:30", espaco_id=4)
    depois = datetime(2026, 10, 25, 22, 30, tzinfo=FUSO_HORARIO)
    contar = ContarReservasAtivasForaDaJanela(repositorio, lambda: depois)
    _salvar(repositorio, S.CONFIRMADA, "21:30", "22:30")

    # Act
    fora = contar.executar(3, MINUTOS_07H, MINUTOS_22H)

    # Assert
    assert fora == 0


def test_reserva_em_andamento_e_contada_pelo_relogio_injetado(repositorio):
    # Arrange
    _salvar(repositorio, S.CONFIRMADA, "21:30", "22:30")
    durante = datetime(2026, 10, 25, 22, 0, tzinfo=FUSO_HORARIO)
    contar = ContarReservasAtivasForaDaJanela(repositorio, lambda: durante)

    # Act / Assert
    assert contar.executar(3, MINUTOS_07H, MINUTOS_22H) == 1
