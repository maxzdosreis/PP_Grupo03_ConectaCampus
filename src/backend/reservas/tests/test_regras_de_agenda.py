from datetime import date, datetime, time, timedelta

import pytest

from compartilhado.api.tratador_de_erros import tratar_excecao
from reservas.domain.excecoes import (
    AntecedenciaExcedida,
    DuracaoInvalida,
    ForaDoHorarioDeFuncionamento,
    HorarioInvalido,
)
from reservas.domain.intervalo_de_horario import FUSO_HORARIO, IntervaloDeHorario
from reservas.domain.regras_de_agenda import (
    ANTECEDENCIA_MAXIMA_EM_DIAS,
    DURACAO_MAXIMA,
    DURACAO_MINIMA,
    DURACAO_SUGERIDA,
    data_limite_para_reservar,
    garantir_regras_de_agenda,
)
from reservas.tests.fakes import (
    AGORA,
    DIA,
    FUNCIONAMENTO_PADRAO,
    UTC,
    exatamente,
    funcionamento,
    fuso_do_processo,
)

DATA_LIMITE = date(2026, 11, 20)
F = FUNCIONAMENTO_PADRAO

PADRAO = ("padrão 07:00–00:00", F)
OITO_A_VINTE_E_DUAS = ("08:00–22:00", funcionamento("08:00", "22:00"))
DEZ_A_QUATORZE = ("10:00–14:00", funcionamento("10:00", "14:00"))

ACEITA = "aceita"
FORA_NO_INICIO = "FORA_DO_HORARIO_DE_FUNCIONAMENTO em hora_inicio"
FORA_NO_TERMINO = "FORA_DO_HORARIO_DE_FUNCIONAMENTO em hora_fim"
DURACAO = "DURACAO_INVALIDA em hora_fim"

BORDAS = [
    (PADRAO, "06:59", "08:00", FORA_NO_INICIO),
    (PADRAO, "07:00", "08:00", ACEITA),
    (PADRAO, "21:00", "22:00", ACEITA),
    (PADRAO, "22:00", "23:00", ACEITA),
    (PADRAO, "23:00", "00:00", ACEITA),
    (PADRAO, "23:30", "00:00", ACEITA),
    (PADRAO, "00:00", "01:00", FORA_NO_INICIO),
    (PADRAO, "10:00", "10:29", DURACAO),
    (PADRAO, "10:00", "10:30", ACEITA),
    (PADRAO, "10:00", "10:31", ACEITA),
    (PADRAO, "10:00", "13:00", ACEITA),
    (PADRAO, "10:00", "13:01", DURACAO),
    (PADRAO, "23:45", "00:00", DURACAO),
    (OITO_A_VINTE_E_DUAS, "07:59", "09:00", FORA_NO_INICIO),
    (OITO_A_VINTE_E_DUAS, "08:00", "09:00", ACEITA),
    (OITO_A_VINTE_E_DUAS, "21:00", "22:00", ACEITA),
    (OITO_A_VINTE_E_DUAS, "21:30", "22:30", FORA_NO_TERMINO),
    (OITO_A_VINTE_E_DUAS, "22:00", "23:00", FORA_NO_TERMINO),
    (OITO_A_VINTE_E_DUAS, "23:00", "00:00", FORA_NO_TERMINO),
    (OITO_A_VINTE_E_DUAS, "00:00", "01:00", FORA_NO_INICIO),
    (OITO_A_VINTE_E_DUAS, "10:00", "10:29", DURACAO),
    (OITO_A_VINTE_E_DUAS, "10:00", "10:30", ACEITA),
    (OITO_A_VINTE_E_DUAS, "10:00", "13:00", ACEITA),
    (OITO_A_VINTE_E_DUAS, "10:00", "13:01", DURACAO),
    (DEZ_A_QUATORZE, "09:59", "11:00", FORA_NO_INICIO),
    (DEZ_A_QUATORZE, "10:00", "11:00", ACEITA),
    (DEZ_A_QUATORZE, "11:00", "14:00", ACEITA),
    (DEZ_A_QUATORZE, "13:30", "14:30", FORA_NO_TERMINO),
    (DEZ_A_QUATORZE, "13:30", "14:00", ACEITA),
    (DEZ_A_QUATORZE, "10:00", "10:29", DURACAO),
    (DEZ_A_QUATORZE, "10:00", "13:01", DURACAO),
    (DEZ_A_QUATORZE, "13:00", "00:00", FORA_NO_TERMINO),
]


def _intervalo(inicio="10:00", fim="11:00", data=DIA):
    return IntervaloDeHorario(
        data=data,
        hora_inicio=time.fromisoformat(inicio),
        hora_fim=time.fromisoformat(fim),
    )


def _rotulo(espaco, inicio, fim, esperado):
    return f"{espaco[0]} | {inicio}–{fim} | {esperado}"


def _aplicar(espaco, inicio, fim, esperado, data, agora):
    intervalo = _intervalo(inicio, fim, data)
    if esperado == ACEITA:
        garantir_regras_de_agenda(intervalo, agora, espaco[1])
        return
    excecao = DuracaoInvalida if esperado == DURACAO else ForaDoHorarioDeFuncionamento
    with pytest.raises(excecao) as erro:
        garantir_regras_de_agenda(intervalo, agora, espaco[1])
    campo = "hora_inicio" if esperado == FORA_NO_INICIO else "hora_fim"
    assert erro.value.campo == campo


@pytest.mark.parametrize(
    ("espaco", "inicio", "fim", "esperado"),
    BORDAS,
    ids=[_rotulo(*linha) for linha in BORDAS],
)
def test_bordas_do_horario_e_da_duracao_por_espaco(espaco, inicio, fim, esperado):
    # Act / Assert
    _aplicar(espaco, inicio, fim, esperado, DIA, AGORA)


DATAS_DE_VIRADA = [
    date(2026, 10, 31),  # a meia-noite vira o mês
    date(2026, 12, 31),  # a meia-noite vira o ano
    date(2028, 2, 29),  # dia bissexto
]


@pytest.mark.parametrize(
    ("espaco", "inicio", "fim", "esperado"),
    BORDAS,
    ids=[_rotulo(*linha) for linha in BORDAS],
)
@pytest.mark.parametrize("data", DATAS_DE_VIRADA, ids=lambda data: data.isoformat())
def test_mesmas_bordas_nas_viradas_de_mes_e_de_ano(espaco, inicio, fim, esperado, data):
    # Arrange
    agora = datetime.combine(data - timedelta(days=3), time(12, 0), tzinfo=FUSO_HORARIO)

    # Act / Assert
    _aplicar(espaco, inicio, fim, esperado, data, agora)


@pytest.mark.parametrize(
    ("espaco", "inicio", "fim", "esperado"),
    BORDAS,
    ids=[_rotulo(*linha) for linha in BORDAS],
)
def test_mesmas_bordas_com_agora_em_utc_que_ja_e_o_dia_seguinte(
    espaco, inicio, fim, esperado
):
    # Arrange: 22:30 em São Paulo na véspera já é o dia seguinte em UTC
    agora_local = datetime.combine(
        DIA - timedelta(days=1), time(22, 30), tzinfo=FUSO_HORARIO
    )
    agora = agora_local.astimezone(UTC)

    # Act / Assert
    assert agora.date() == DIA
    _aplicar(espaco, inicio, fim, esperado, DIA, agora)


def test_reserva_das_23_as_00_cruza_o_dia_em_utc_mas_continua_no_dia_local():
    # Arrange
    intervalo = _intervalo("23:00", "00:00")

    # Act
    garantir_regras_de_agenda(intervalo, AGORA, F)

    # Assert
    assert intervalo.data == DIA
    assert intervalo.inicio().astimezone(UTC).date() == DIA + timedelta(days=1)
    assert intervalo.fim() - intervalo.inicio() == timedelta(hours=1)
    assert intervalo.fim().astimezone(FUSO_HORARIO).date() == DIA + timedelta(days=1)


@pytest.mark.parametrize(
    ("inicio", "fim"),
    [("23:30", "00:30"), ("23:00", "01:00")],
    ids=["23h30-as-00h30", "23h-as-01h"],
)
def test_termino_depois_da_meia_noite_nao_vira_o_dia(inicio, fim):
    # Act / Assert
    with pytest.raises(HorarioInvalido):
        _intervalo(inicio, fim)


def test_inicio_e_termino_as_00_00_e_o_dia_inteiro_e_nao_uma_reserva_valida():
    # Arrange: 00:00 como término é 24:00, então 00:00–00:00 dura 24 horas
    intervalo = _intervalo("00:00", "00:00")

    # Act
    with pytest.raises(ForaDoHorarioDeFuncionamento) as no_padrao:
        garantir_regras_de_agenda(intervalo, AGORA, F)
    with pytest.raises(DuracaoInvalida):
        garantir_regras_de_agenda(intervalo, AGORA, funcionamento("00:00", "00:00"))

    # Assert
    assert intervalo.fim() - intervalo.inicio() == timedelta(hours=24)
    assert no_padrao.value.campo == "hora_inicio"


def test_mensagem_de_fora_do_horario_cita_o_horario_do_espaco():
    # Act
    with pytest.raises(ForaDoHorarioDeFuncionamento) as padrao:
        garantir_regras_de_agenda(_intervalo("06:00", "08:00"), AGORA, F)
    with pytest.raises(ForaDoHorarioDeFuncionamento) as proprio:
        garantir_regras_de_agenda(
            _intervalo("17:30", "18:30"), AGORA, funcionamento("08:00", "18:00")
        )

    # Assert
    assert padrao.value.codigo == "FORA_DO_HORARIO_DE_FUNCIONAMENTO"
    assert padrao.value.mensagem == (
        "O espaço funciona das 07:00 às 00:00. Escolha um horário dentro desse período."
    )
    assert proprio.value.campo == "hora_fim"
    assert proprio.value.mensagem == (
        "O espaço funciona das 08:00 às 18:00. Escolha um horário dentro desse período."
    )


@pytest.mark.parametrize(
    ("limite", "combinado"),
    [
        (DURACAO_SUGERIDA, timedelta(hours=1)),
        (DURACAO_MINIMA, timedelta(minutes=30)),
        (DURACAO_MAXIMA, timedelta(hours=3)),
        (ANTECEDENCIA_MAXIMA_EM_DIAS, 30),
    ],
    ids=["duracao-sugerida", "duracao-minima", "duracao-maxima", "antecedencia"],
)
def test_os_limites_sao_os_combinados_com_o_grupo(limite, combinado):
    # Assert
    assert limite == combinado


def test_duracao_sugerida_e_so_sugestao_e_45_minutos_continua_valido():
    # Act / Assert
    garantir_regras_de_agenda(_intervalo("10:00", "10:45"), AGORA, F)


@pytest.mark.parametrize("fim", ["10:20", "10:29"], ids=["20-minutos", "29-minutos"])
def test_duracao_menor_que_o_minimo_segue_recusada_com_a_mensagem_de_sempre(fim):
    # Act
    with pytest.raises(DuracaoInvalida) as erro:
        garantir_regras_de_agenda(_intervalo("10:00", fim), AGORA, F)

    # Assert
    assert erro.value.campo == "hora_fim"
    assert erro.value.codigo == "DURACAO_INVALIDA"
    assert erro.value.mensagem == "A reserva deve durar entre 30 minutos e 3 horas."


@pytest.mark.parametrize(
    ("minima", "maxima", "mensagem"),
    [
        (
            timedelta(minutes=1),
            timedelta(hours=1, minutes=30),
            "A reserva deve durar entre 1 minuto e 1 hora e 30 minutos.",
        ),
        (
            timedelta(hours=2),
            timedelta(hours=4, minutes=1),
            "A reserva deve durar entre 2 horas e 4 horas e 1 minuto.",
        ),
    ],
    ids=["singular", "plural"],
)
def test_mensagem_de_duracao_descreve_horas_e_minutos(minima, maxima, mensagem):
    # Act
    erro = DuracaoInvalida(minima, maxima)

    # Assert
    assert erro.mensagem == mensagem


def test_data_no_limite_da_antecedencia_e_aceita_inclusive_ate_a_meia_noite():
    # Act / Assert
    garantir_regras_de_agenda(
        _intervalo("23:00", "00:00", data=AGORA.date() + timedelta(days=30)), AGORA, F
    )


def test_data_alem_da_antecedencia_e_recusada_com_a_data_limite():
    # Act
    with pytest.raises(AntecedenciaExcedida) as erro:
        garantir_regras_de_agenda(
            _intervalo(data=AGORA.date() + timedelta(days=31)), AGORA, F
        )

    # Assert
    assert erro.value.campo == "data"
    assert erro.value.codigo == "ANTECEDENCIA_EXCEDIDA"
    assert erro.value.data_limite == DATA_LIMITE
    assert erro.value.mensagem == (
        "Só é possível reservar com até 30 dias de antecedência (até 20/11/2026)."
    )


def test_primeira_regra_violada_vem_na_ordem_funcionamento_duracao_antecedencia():
    # Arrange
    intervalo = _intervalo("06:00", "06:10", data=AGORA.date() + timedelta(days=31))

    # Act / Assert
    with pytest.raises(ForaDoHorarioDeFuncionamento):
        garantir_regras_de_agenda(intervalo, AGORA, F)
    intervalo = _intervalo("10:00", "10:10", data=AGORA.date() + timedelta(days=31))
    with pytest.raises(DuracaoInvalida):
        garantir_regras_de_agenda(intervalo, AGORA, F)


def test_data_limite_conta_hoje_no_fuso_de_sao_paulo():
    # Arrange
    noite_em_sao_paulo = datetime(2026, 10, 21, 23, 30, tzinfo=FUSO_HORARIO)
    mesmo_instante_em_utc = noite_em_sao_paulo.astimezone(UTC)

    # Act
    limite = data_limite_para_reservar(mesmo_instante_em_utc)

    # Assert
    assert mesmo_instante_em_utc.date() == date(2026, 10, 22)
    assert limite == DATA_LIMITE


def test_virada_do_dia_em_utc_nao_muda_a_antecedencia():
    # Arrange
    agora_em_utc = datetime(2026, 10, 21, 23, 30, tzinfo=FUSO_HORARIO).astimezone(UTC)

    # Act / Assert
    garantir_regras_de_agenda(_intervalo(data=DATA_LIMITE), agora_em_utc, F)
    with pytest.raises(AntecedenciaExcedida):
        garantir_regras_de_agenda(
            _intervalo(data=DATA_LIMITE + timedelta(days=1)), agora_em_utc, F
        )


@pytest.mark.parametrize("agora", [datetime(2026, 10, 21, 12, 0), None])
def test_data_limite_com_agora_sem_fuso_e_erro_de_programacao(agora):
    # Act / Assert
    with pytest.raises(
        TypeError, match=exatamente("agora deve ser um datetime com fuso horário.")
    ):
        data_limite_para_reservar(agora)


def test_data_limite_nao_depende_do_fuso_do_processo():
    # Arrange
    noite_em_sao_paulo = datetime(2026, 10, 21, 23, 30, tzinfo=FUSO_HORARIO)

    # Act
    with fuso_do_processo("UTC"):
        limite = data_limite_para_reservar(noite_em_sao_paulo)

    # Assert
    assert limite == DATA_LIMITE


@pytest.mark.parametrize(
    ("erro", "codigo", "campo"),
    [
        (
            ForaDoHorarioDeFuncionamento("hora_inicio", time(7, 0), time(0, 0)),
            "FORA_DO_HORARIO_DE_FUNCIONAMENTO",
            "hora_inicio",
        ),
        (
            ForaDoHorarioDeFuncionamento("hora_fim", time(7, 0), time(0, 0)),
            "FORA_DO_HORARIO_DE_FUNCIONAMENTO",
            "hora_fim",
        ),
        (
            DuracaoInvalida(DURACAO_MINIMA, DURACAO_MAXIMA),
            "DURACAO_INVALIDA",
            "hora_fim",
        ),
        (
            AntecedenciaExcedida(ANTECEDENCIA_MAXIMA_EM_DIAS, DATA_LIMITE),
            "ANTECEDENCIA_EXCEDIDA",
            "data",
        ),
    ],
    ids=["abertura", "fechamento", "duracao", "antecedencia"],
)
def test_erros_de_agenda_viram_400_marcando_o_campo(erro, codigo, campo):
    # Act
    resposta = tratar_excecao(erro, {})

    # Assert
    assert resposta.status_code == 400
    assert resposta.data == {
        "erro": {
            "codigo": codigo,
            "mensagem": erro.mensagem,
            "campos": {campo: [erro.mensagem]},
        }
    }
