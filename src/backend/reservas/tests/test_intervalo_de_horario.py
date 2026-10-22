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


CASOS_DE_SOBREPOSICAO = [
    pytest.param(time(10, 0), time(11, 0), True, id="iguais"),
    pytest.param(time(10, 15), time(10, 45), True, id="contido"),
    pytest.param(time(9, 0), time(12, 0), True, id="contendo"),
    pytest.param(time(9, 30), time(10, 30), True, id="parcial-no-inicio"),
    pytest.param(time(10, 30), time(11, 30), True, id="parcial-no-fim"),
    pytest.param(time(9, 0), time(10, 0), False, id="encostado-antes"),
    pytest.param(time(11, 0), time(12, 0), False, id="encostado-depois"),
]


@pytest.mark.parametrize(("hora_inicio", "hora_fim", "esperado"), CASOS_DE_SOBREPOSICAO)
def test_sobrepoe_compara_os_horarios_como_intervalo_semiaberto(
    hora_inicio, hora_fim, esperado
):
    # Arrange
    base = _criar_intervalo()
    outro = _criar_intervalo(hora_inicio=hora_inicio, hora_fim=hora_fim)

    # Act
    sobrepoe = base.sobrepoe(outro)

    # Assert
    assert sobrepoe is esperado


@pytest.mark.parametrize(("hora_inicio", "hora_fim", "esperado"), CASOS_DE_SOBREPOSICAO)
def test_sobrepoe_e_simetrico(hora_inicio, hora_fim, esperado):
    # Arrange
    base = _criar_intervalo()
    outro = _criar_intervalo(hora_inicio=hora_inicio, hora_fim=hora_fim)

    # Assert
    assert base.sobrepoe(outro) is outro.sobrepoe(base) is esperado


def test_mesmo_horario_em_datas_diferentes_nao_se_sobrepoe():
    # Arrange
    base = _criar_intervalo()
    dia_seguinte = _criar_intervalo(data=date(2026, 10, 26))

    # Assert
    assert base.sobrepoe(dia_seguinte) is False
    assert dia_seguinte.sobrepoe(base) is False
