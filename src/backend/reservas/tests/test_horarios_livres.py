from datetime import date, datetime, time, timedelta

import pytest

from reservas.domain.excecoes import AntecedenciaExcedida, DataRetroativa
from reservas.domain.intervalo_de_horario import FUSO_HORARIO
from reservas.domain.regras_de_agenda import (
    garantir_data_reservavel,
    horarios_livres,
    motivo_de_indisponibilidade,
)
from reservas.tests.fakes import AGORA, UTC, exatamente, fuso_do_processo, intervalo

HOJE = AGORA.date()
AMANHA = HOJE + timedelta(days=1)


def _ocupado(inicio, fim, data=AMANHA):
    return intervalo(inicio, fim, data)


def _como_texto(livres):
    return [f"{livre.hora_inicio:%H:%M}–{livre.hora_fim:%H:%M}" for livre in livres]


def _agora_hoje(hora):
    return datetime.combine(HOJE, time.fromisoformat(hora), tzinfo=FUSO_HORARIO)


@pytest.mark.parametrize(
    ("ocupados", "esperado"),
    [
        ([], ["07:00–22:00"]),
        ([("07:00", "09:00")], ["09:00–22:00"]),
        ([("12:00", "13:30")], ["07:00–12:00", "13:30–22:00"]),
        ([("20:00", "22:00")], ["07:00–20:00"]),
        ([("10:00", "11:00"), ("11:00", "12:00")], ["07:00–10:00", "12:00–22:00"]),
        (
            [("15:00", "16:00"), ("08:00", "09:00"), ("11:00", "12:00")],
            ["07:00–08:00", "09:00–11:00", "12:00–15:00", "16:00–22:00"],
        ),
        ([("10:00", "12:00"), ("11:00", "11:30")], ["07:00–10:00", "12:00–22:00"]),
    ],
    ids=[
        "sem-ocupados",
        "ocupado-no-comeco",
        "ocupado-no-meio",
        "ocupado-no-fim",
        "ocupados-encostados",
        "ocupados-fora-de-ordem",
        "ocupado-dentro-de-outro",
    ],
)
def test_livres_sao_o_funcionamento_menos_os_ocupados(ocupados, esperado):
    # Arrange
    intervalos = [_ocupado(inicio, fim) for inicio, fim in ocupados]

    # Act
    livres = horarios_livres(intervalos, data=AMANHA, agora=AGORA)

    # Assert
    assert _como_texto(livres) == esperado
    assert all(livre.data == AMANHA for livre in livres)


def test_janela_de_20_minutos_entre_dois_ocupados_nao_aparece():
    # Arrange
    intervalos = [_ocupado("09:00", "10:40"), _ocupado("11:00", "12:00")]

    # Act
    livres = horarios_livres(intervalos, data=AMANHA, agora=AGORA)

    # Assert
    assert _como_texto(livres) == ["07:00–09:00", "12:00–22:00"]


def test_janela_de_30_minutos_entre_dois_ocupados_aparece():
    # Arrange
    intervalos = [_ocupado("09:00", "10:30"), _ocupado("11:00", "12:00")]

    # Act
    livres = horarios_livres(intervalos, data=AMANHA, agora=AGORA)

    # Assert
    assert _como_texto(livres) == ["07:00–09:00", "10:30–11:00", "12:00–22:00"]


@pytest.mark.parametrize(
    ("agora", "inicio"),
    [
        ("15:37", time(15, 40)),
        ("15:37:59", time(15, 40)),
        ("15:37:59.500000", time(15, 40)),
        ("15:40", time(15, 45)),
        ("06:12", time(7, 0)),
    ],
    ids=[
        "15h37",
        "15h37-e-59s",
        "15h37-59s-e-meio",
        "exatamente-15h40",
        "antes-da-abertura",
    ],
)
def test_hoje_a_primeira_janela_comeca_no_proximo_multiplo_de_5_minutos(agora, inicio):
    # Act
    livres = horarios_livres([], data=HOJE, agora=_agora_hoje(agora))

    # Assert
    assert [(livre.hora_inicio, livre.hora_fim) for livre in livres] == [
        (inicio, time(22, 0))
    ]


def test_hoje_o_passado_e_recortado_antes_dos_ocupados():
    # Arrange
    intervalos = [_ocupado("14:00", "16:00", data=HOJE)]

    # Act
    livres = horarios_livres(intervalos, data=HOJE, agora=_agora_hoje("15:37"))

    # Assert
    assert _como_texto(livres) == ["16:00–22:00"]


def test_agora_em_utc_e_lido_no_fuso_de_sao_paulo():
    # Arrange
    agora_em_utc = _agora_hoje("15:37").astimezone(UTC)

    # Act
    livres = horarios_livres([], data=HOJE, agora=agora_em_utc)

    # Assert
    assert _como_texto(livres) == ["15:40–22:00"]


def test_primeira_janela_de_hoje_nao_depende_do_fuso_do_processo():
    # Arrange
    agora_em_utc = _agora_hoje("15:37").astimezone(UTC)

    # Act
    with fuso_do_processo("UTC"):
        livres = horarios_livres([], data=HOJE, agora=agora_em_utc)

    # Assert
    assert _como_texto(livres) == ["15:40–22:00"]


@pytest.mark.parametrize(
    "agora", ["21:31", "22:00", "23:58"], ids=["sem-30-minutos", "fechou", "noite"]
)
def test_hoje_perto_ou_depois_do_fechamento_nao_ha_livres(agora):
    # Act
    livres = horarios_livres([], data=HOJE, agora=_agora_hoje(agora))

    # Assert
    assert livres == []


def test_data_passada_nao_tem_livres():
    # Act
    livres = horarios_livres([], data=HOJE - timedelta(days=1), agora=AGORA)

    # Assert
    assert livres == []


def test_livres_com_agora_sem_fuso_e_erro_de_programacao():
    # Act / Assert
    with pytest.raises(
        TypeError, match=exatamente("agora deve ser um datetime com fuso horário.")
    ):
        horarios_livres([], data=AMANHA, agora=datetime(2026, 10, 21, 12, 0))


DATAS_CUJO_FUNCIONAMENTO_JA_ACABOU = pytest.mark.parametrize(
    ("data", "agora"),
    [
        (HOJE - timedelta(days=1), AGORA),
        (HOJE, _agora_hoje("22:00")),
        (HOJE, _agora_hoje("22:30")),
    ],
    ids=["ontem", "hoje-no-fechamento", "hoje-depois-do-fechamento"],
)


@DATAS_CUJO_FUNCIONAMENTO_JA_ACABOU
def test_data_cujo_funcionamento_ja_acabou_e_retroativa(data, agora):
    # Act / Assert
    with pytest.raises(DataRetroativa):
        garantir_data_reservavel(data, agora)


@DATAS_CUJO_FUNCIONAMENTO_JA_ACABOU
def test_data_cujo_funcionamento_ja_acabou_traz_o_motivo_de_data_retroativa(
    data, agora
):
    # Act
    motivo = motivo_de_indisponibilidade(data, agora)

    # Assert
    assert motivo == DataRetroativa().mensagem


def test_data_alem_da_antecedencia_e_recusada():
    # Act
    with pytest.raises(AntecedenciaExcedida) as erro:
        garantir_data_reservavel(HOJE + timedelta(days=31), AGORA)

    # Assert
    assert erro.value.data_limite == date(2026, 11, 20)


def test_data_alem_da_antecedencia_traz_a_mensagem_com_a_data_limite():
    # Act
    motivo = motivo_de_indisponibilidade(HOJE + timedelta(days=31), AGORA)

    # Assert
    assert motivo == (
        "Só é possível reservar com até 30 dias de antecedência (até 20/11/2026)."
    )


@pytest.mark.parametrize(
    ("data", "agora"),
    [
        (AMANHA, AGORA),
        (HOJE + timedelta(days=30), AGORA),
        (HOJE, _agora_hoje("21:59")),
    ],
    ids=["amanha", "no-limite-da-antecedencia", "hoje-antes-do-fechamento"],
)
def test_data_reservavel_nao_tem_motivo(data, agora):
    # Act
    motivo = motivo_de_indisponibilidade(data, agora)

    # Assert
    assert motivo is None


def test_disponibilidade_com_agora_sem_fuso_e_erro_de_programacao():
    # Act / Assert
    with pytest.raises(
        TypeError, match=exatamente("agora deve ser um datetime com fuso horário.")
    ):
        motivo_de_indisponibilidade(AMANHA, datetime(2026, 10, 21, 12, 0))
