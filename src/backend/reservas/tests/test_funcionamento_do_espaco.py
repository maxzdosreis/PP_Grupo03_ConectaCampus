from datetime import date, datetime, time, timedelta

import pytest

from reservas.domain.funcionamento import MINUTOS_NO_DIA, FuncionamentoDoEspaco
from reservas.domain.intervalo_de_horario import FUSO_HORARIO, IntervaloDeHorario
from reservas.tests.fakes import UTC, funcionamento

DIA = date(2026, 12, 31)


def test_fechamento_1440_e_a_meia_noite_do_fim_do_dia():
    # Act
    padrao = funcionamento("07:00", "00:00")

    # Assert
    assert padrao.fechamento_em_minutos == MINUTOS_NO_DIA
    assert padrao.abertura() == time(7, 0)
    assert padrao.fechamento() == time(0, 0)
    assert padrao.abre_em(DIA) == datetime(2026, 12, 31, 7, 0, tzinfo=FUSO_HORARIO)
    assert padrao.fecha_em(DIA) == datetime(2027, 1, 1, 0, 0, tzinfo=FUSO_HORARIO)


def test_fechamento_proprio_fecha_no_mesmo_dia():
    # Act
    de_dia = funcionamento("08:00", "22:00")

    # Assert
    assert de_dia.fecha_em(DIA) == datetime(2026, 12, 31, 22, 0, tzinfo=FUSO_HORARIO)


def test_funcionamento_e_comparado_em_datetimes_com_fuso_e_nao_em_utc():
    # Arrange
    padrao = funcionamento("07:00", "00:00")
    intervalo = IntervaloDeHorario(
        data=DIA, hora_inicio=time(23, 0), hora_fim=time(0, 0)
    )

    # Assert
    assert intervalo.inicio().astimezone(UTC).date() == date(2027, 1, 1)
    assert padrao.abre_em(DIA) <= intervalo.inicio()
    assert intervalo.fim() <= padrao.fecha_em(DIA)


@pytest.mark.parametrize(
    ("abertura", "fechamento"),
    [(-1, 600), (600, 600), (700, 600), (0, 1441)],
    ids=["abertura-negativa", "janela-vazia", "fecha-antes-de-abrir", "alem-de-24h"],
)
def test_funcionamento_fora_da_convencao_e_erro_de_programacao(abertura, fechamento):
    # Act / Assert
    with pytest.raises(ValueError, match="funcionamento|fechamento"):
        FuncionamentoDoEspaco(abertura, fechamento)


def test_o_dia_inteiro_e_um_funcionamento_valido():
    # Act
    dia_inteiro = FuncionamentoDoEspaco(0, MINUTOS_NO_DIA)

    # Assert
    assert dia_inteiro.abertura() == time(0, 0)
    assert dia_inteiro.fechamento() == time(0, 0)
    assert dia_inteiro.fecha_em(DIA) - dia_inteiro.abre_em(DIA) == timedelta(hours=24)
