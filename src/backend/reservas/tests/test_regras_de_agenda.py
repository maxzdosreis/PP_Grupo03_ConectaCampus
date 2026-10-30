from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest

from compartilhado.api.tratador_de_erros import tratar_excecao
from reservas.domain.excecoes import (
    AntecedenciaExcedida,
    DuracaoInvalida,
    ForaDoHorarioDeFuncionamento,
)
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.regras_de_agenda import (
    ANTECEDENCIA_MAXIMA_EM_DIAS,
    DURACAO_MAXIMA,
    DURACAO_MINIMA,
    HORARIO_DE_ABERTURA,
    HORARIO_DE_FECHAMENTO,
    data_limite_para_reservar,
    garantir_regras_de_agenda,
)

SAO_PAULO = ZoneInfo("America/Sao_Paulo")
UTC = ZoneInfo("UTC")
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=SAO_PAULO)
DATA = AGORA.date() + timedelta(days=4)
DATA_LIMITE = date(2026, 11, 20)


def _intervalo(hora_inicio=time(10, 0), hora_fim=time(11, 0), data=DATA):
    return IntervaloDeHorario(data=data, hora_inicio=hora_inicio, hora_fim=hora_fim)


@pytest.mark.parametrize(
    ("limite", "combinado"),
    [
        (HORARIO_DE_ABERTURA, time(7, 0)),
        (HORARIO_DE_FECHAMENTO, time(22, 0)),
        (DURACAO_MINIMA, timedelta(minutes=30)),
        (DURACAO_MAXIMA, timedelta(hours=3)),
        (ANTECEDENCIA_MAXIMA_EM_DIAS, 30),
    ],
    ids=["abertura", "fechamento", "duracao-minima", "duracao-maxima", "antecedencia"],
)
def test_os_limites_sao_os_combinados_com_o_grupo(limite, combinado):
    # Assert
    assert limite == combinado


@pytest.mark.parametrize(
    ("hora_inicio", "hora_fim"),
    [(time(7, 0), time(8, 0)), (time(21, 0), time(22, 0))],
    ids=["comeca-na-abertura", "termina-no-fechamento"],
)
def test_horario_nas_bordas_do_funcionamento_e_aceito(hora_inicio, hora_fim):
    # Act / Assert
    garantir_regras_de_agenda(_intervalo(hora_inicio, hora_fim), AGORA)


@pytest.mark.parametrize(
    ("hora_inicio", "hora_fim", "campo"),
    [
        (time(6, 59), time(8, 0), "hora_inicio"),
        (time(21, 0), time(22, 1), "hora_fim"),
    ],
    ids=["comeca-antes-da-abertura", "termina-depois-do-fechamento"],
)
def test_horario_fora_do_funcionamento_e_recusado_no_campo_certo(
    hora_inicio, hora_fim, campo
):
    # Act
    with pytest.raises(ForaDoHorarioDeFuncionamento) as erro:
        garantir_regras_de_agenda(_intervalo(hora_inicio, hora_fim), AGORA)

    # Assert
    assert erro.value.campo == campo
    assert erro.value.codigo == "FORA_DO_HORARIO_DE_FUNCIONAMENTO"
    assert erro.value.mensagem == (
        "Os espaços funcionam das 07:00 às 22:00. "
        "Escolha um horário dentro desse período."
    )


@pytest.mark.parametrize(
    "hora_fim", [time(10, 30), time(13, 0)], ids=["30-minutos", "3-horas"]
)
def test_duracao_nas_bordas_e_aceita(hora_fim):
    # Act / Assert
    garantir_regras_de_agenda(_intervalo(time(10, 0), hora_fim), AGORA)


@pytest.mark.parametrize(
    "hora_fim", [time(10, 29), time(13, 1)], ids=["29-minutos", "3-horas-e-1-minuto"]
)
def test_duracao_fora_dos_limites_e_recusada_no_termino(hora_fim):
    # Act
    with pytest.raises(DuracaoInvalida) as erro:
        garantir_regras_de_agenda(_intervalo(time(10, 0), hora_fim), AGORA)

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


def test_data_no_limite_da_antecedencia_e_aceita():
    # Act / Assert
    garantir_regras_de_agenda(_intervalo(data=AGORA.date() + timedelta(days=30)), AGORA)


def test_data_alem_da_antecedencia_e_recusada_com_a_data_limite():
    # Act
    with pytest.raises(AntecedenciaExcedida) as erro:
        garantir_regras_de_agenda(
            _intervalo(data=AGORA.date() + timedelta(days=31)), AGORA
        )

    # Assert
    assert erro.value.campo == "data"
    assert erro.value.codigo == "ANTECEDENCIA_EXCEDIDA"
    assert erro.value.data_limite == DATA_LIMITE
    assert erro.value.mensagem == (
        "Só é possível reservar com até 30 dias de antecedência (até 20/11/2026)."
    )


def test_data_limite_conta_hoje_no_fuso_de_sao_paulo():
    # Arrange
    noite_em_sao_paulo = datetime(2026, 10, 21, 23, 30, tzinfo=SAO_PAULO)
    mesmo_instante_em_utc = noite_em_sao_paulo.astimezone(UTC)

    # Act
    limite = data_limite_para_reservar(mesmo_instante_em_utc)

    # Assert
    assert mesmo_instante_em_utc.date() == date(2026, 10, 22)
    assert limite == DATA_LIMITE


def test_virada_do_dia_em_utc_nao_muda_a_antecedencia():
    # Arrange
    agora_em_utc = datetime(2026, 10, 21, 23, 30, tzinfo=SAO_PAULO).astimezone(UTC)

    # Act / Assert
    garantir_regras_de_agenda(_intervalo(data=DATA_LIMITE), agora_em_utc)
    with pytest.raises(AntecedenciaExcedida):
        garantir_regras_de_agenda(
            _intervalo(data=DATA_LIMITE + timedelta(days=1)), agora_em_utc
        )


@pytest.mark.parametrize("agora", [datetime(2026, 10, 21, 12, 0), None])
def test_data_limite_com_agora_sem_fuso_e_erro_de_programacao(agora):
    # Act / Assert
    with pytest.raises(TypeError):
        data_limite_para_reservar(agora)


@pytest.mark.parametrize(
    ("erro", "codigo", "campo"),
    [
        (
            ForaDoHorarioDeFuncionamento(
                "hora_inicio", HORARIO_DE_ABERTURA, HORARIO_DE_FECHAMENTO
            ),
            "FORA_DO_HORARIO_DE_FUNCIONAMENTO",
            "hora_inicio",
        ),
        (
            ForaDoHorarioDeFuncionamento(
                "hora_fim", HORARIO_DE_ABERTURA, HORARIO_DE_FECHAMENTO
            ),
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
