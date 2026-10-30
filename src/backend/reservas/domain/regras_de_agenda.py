from collections.abc import Iterable, Iterator
from datetime import date, datetime, time, timedelta

from reservas.domain.excecoes import (
    AntecedenciaExcedida,
    DataRetroativa,
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
GRANULARIDADE_DOS_HORARIOS_LIVRES = timedelta(minutes=5)


def garantir_regras_de_agenda(intervalo: IntervaloDeHorario, agora: datetime) -> None:
    _garantir_horario_de_funcionamento(intervalo)
    _garantir_duracao(intervalo)
    _garantir_antecedencia(intervalo.data, agora)


def data_limite_para_reservar(agora: datetime) -> date:
    exigir_fuso(agora, "agora")
    hoje = agora.astimezone(FUSO_HORARIO).date()
    return hoje + timedelta(days=ANTECEDENCIA_MAXIMA_EM_DIAS)


def garantir_data_reservavel(data: date, agora: datetime) -> None:
    exigir_fuso(agora, "agora")
    if _no_horario(data, HORARIO_DE_FECHAMENTO) <= agora:
        raise DataRetroativa()
    _garantir_antecedencia(data, agora)


def motivo_de_indisponibilidade(data: date, agora: datetime) -> str | None:
    try:
        garantir_data_reservavel(data, agora)
    except (DataRetroativa, AntecedenciaExcedida) as erro:
        return erro.mensagem
    return None


def horarios_livres(
    ocupados: Iterable[IntervaloDeHorario], *, data: date, agora: datetime
) -> list[IntervaloDeHorario]:
    exigir_fuso(agora, "agora")
    janelas = _janelas_entre(
        sorted(ocupados, key=IntervaloDeHorario.inicio),
        _primeiro_inicio_possivel(data, agora),
        _no_horario(data, HORARIO_DE_FECHAMENTO),
    )
    return [
        IntervaloDeHorario(data=data, hora_inicio=inicio.time(), hora_fim=fim.time())
        for inicio, fim in janelas
        if fim - inicio >= DURACAO_MINIMA
    ]


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


def _garantir_antecedencia(data: date, agora: datetime) -> None:
    data_limite = data_limite_para_reservar(agora)
    if data > data_limite:
        raise AntecedenciaExcedida(ANTECEDENCIA_MAXIMA_EM_DIAS, data_limite)


def _no_horario(data: date, horario: time) -> datetime:
    return datetime.combine(data, horario, tzinfo=FUSO_HORARIO)


def _primeiro_inicio_possivel(data: date, agora: datetime) -> datetime:
    return max(_no_horario(data, HORARIO_DE_ABERTURA), _proximo_inicio_redondo(agora))


def _proximo_inicio_redondo(agora: datetime) -> datetime:
    local = agora.astimezone(FUSO_HORARIO).replace(second=0, microsecond=0)
    passado = (local - local.replace(minute=0)) % GRANULARIDADE_DOS_HORARIOS_LIVRES
    return local - passado + GRANULARIDADE_DOS_HORARIOS_LIVRES


def _janelas_entre(
    ocupados: list[IntervaloDeHorario], inicio: datetime, fim: datetime
) -> Iterator[tuple[datetime, datetime]]:
    cursor = inicio
    for ocupado in ocupados:
        if ocupado.inicio() > cursor:
            yield cursor, min(ocupado.inicio(), fim)
        cursor = max(cursor, ocupado.fim())
    yield cursor, fim
