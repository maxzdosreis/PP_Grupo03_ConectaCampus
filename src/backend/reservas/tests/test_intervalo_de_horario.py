from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest

from compartilhado.domain.erros import CampoObrigatorioAusente
from reservas.domain.excecoes import HorarioInvalido
from reservas.domain.intervalo_de_horario import FUSO_HORARIO, IntervaloDeHorario

SAO_PAULO = ZoneInfo("America/Sao_Paulo")


def _criar_intervalo(**sobrescritas):
    dados = {
        "data": date(2026, 10, 25),
        "hora_inicio": time(10, 0),
        "hora_fim": time(11, 0),
    }
    dados.update(sobrescritas)
    return IntervaloDeHorario(**dados)


def test_fuso_horario_e_o_de_sao_paulo():
    # Assert
    assert FUSO_HORARIO == SAO_PAULO


@pytest.mark.parametrize("campo", ["data", "hora_inicio", "hora_fim"])
def test_campo_vazio_e_recusado_como_obrigatorio(campo):
    # Act
    with pytest.raises(CampoObrigatorioAusente) as erro:
        _criar_intervalo(**{campo: None})

    # Assert
    assert erro.value.campo == campo


@pytest.mark.parametrize("hora_fim", [time(10, 0), time(9, 59)])
def test_fim_igual_ou_antes_do_inicio_e_recusado(hora_fim):
    # Act
    with pytest.raises(HorarioInvalido) as erro:
        _criar_intervalo(hora_fim=hora_fim)

    # Assert
    assert erro.value.campo == "hora_fim"
    assert erro.value.mensagem == (
        "O horário de término deve ser posterior ao de início."
    )


def test_datetime_no_lugar_de_date_e_recusado():
    # Act / Assert
    with pytest.raises(TypeError):
        _criar_intervalo(data=datetime(2026, 10, 25, 10, 0))


@pytest.mark.parametrize("campo", ["hora_inicio", "hora_fim"])
def test_hora_que_nao_e_time_e_recusada(campo):
    # Act / Assert
    with pytest.raises(TypeError):
        _criar_intervalo(**{campo: "10:00"})


def test_inicio_combina_data_e_hora_com_fuso_de_sao_paulo():
    # Act
    inicio = _criar_intervalo().inicio()

    # Assert
    assert inicio == datetime(2026, 10, 25, 10, 0, tzinfo=SAO_PAULO)
    assert inicio.tzinfo == SAO_PAULO
    assert inicio.utcoffset() == timedelta(hours=-3)


def test_fim_combina_data_e_hora_com_fuso_de_sao_paulo():
    # Act
    fim = _criar_intervalo().fim()

    # Assert
    assert fim == datetime(2026, 10, 25, 11, 0, tzinfo=SAO_PAULO)
    assert fim.tzinfo == SAO_PAULO


def test_str_mostra_data_e_horarios():
    # Assert
    assert str(_criar_intervalo()) == "25/10/2026 10:00–11:00"
