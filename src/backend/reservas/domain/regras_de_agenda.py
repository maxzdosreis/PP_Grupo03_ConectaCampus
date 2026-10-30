from datetime import date, datetime, time, timedelta

from reservas.domain.excecoes import (
    AntecedenciaExcedida,
    DuracaoInvalida,
    ForaDoHorarioDeFuncionamento,
)
from reservas.domain.intervalo_de_horario import FUSO_HORARIO, IntervaloDeHorario
from reservas.domain.momento import exigir_fuso

HORARIO_DE_ABERTURA = time(7, 0)
HORARIO_DE_FECHAMENTO = time(22, 0)
DURACAO_MINIMA = timedelta(minutes=30)
DURACAO_MAXIMA = timedelta(hours=3)
ANTECEDENCIA_MAXIMA_EM_DIAS = 30


def garantir_regras_de_agenda(intervalo: IntervaloDeHorario, agora: datetime) -> None:
    _garantir_horario_de_funcionamento(intervalo)
    _garantir_duracao(intervalo)
    _garantir_antecedencia(intervalo, agora)


def data_limite_para_reservar(agora: datetime) -> date:
    exigir_fuso(agora, "agora")
    hoje = agora.astimezone(FUSO_HORARIO).date()
    return hoje + timedelta(days=ANTECEDENCIA_MAXIMA_EM_DIAS)


def _garantir_horario_de_funcionamento(intervalo: IntervaloDeHorario) -> None:
    if intervalo.hora_inicio < HORARIO_DE_ABERTURA:
        raise ForaDoHorarioDeFuncionamento(
            "hora_inicio", HORARIO_DE_ABERTURA, HORARIO_DE_FECHAMENTO
        )
    if intervalo.hora_fim > HORARIO_DE_FECHAMENTO:
        raise ForaDoHorarioDeFuncionamento(
            "hora_fim", HORARIO_DE_ABERTURA, HORARIO_DE_FECHAMENTO
        )


def _garantir_duracao(intervalo: IntervaloDeHorario) -> None:
    duracao = intervalo.fim() - intervalo.inicio()
    if not DURACAO_MINIMA <= duracao <= DURACAO_MAXIMA:
        raise DuracaoInvalida(DURACAO_MINIMA, DURACAO_MAXIMA)


def _garantir_antecedencia(intervalo: IntervaloDeHorario, agora: datetime) -> None:
    data_limite = data_limite_para_reservar(agora)
    if intervalo.data > data_limite:
        raise AntecedenciaExcedida(ANTECEDENCIA_MAXIMA_EM_DIAS, data_limite)
