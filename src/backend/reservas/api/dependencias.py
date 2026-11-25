from collections.abc import Callable
from datetime import datetime

from django.utils import timezone

from reservas.application.casos_de_uso import (
    AlterarSituacaoReserva,
    ConsultarHistoricoDaReserva,
    ConsultarOcupacaoDoDia,
    ConsultarReservas,
    ContarReservasAtivasForaDaJanela,
    CriarReserva,
    ObterReserva,
)
from reservas.application.reconstruir_agenda import ReconstruirAgenda
from reservas.infrastructure.agenda_redis import AgendaDoDiaRedis
from reservas.infrastructure.consulta_de_espacos import ConsultaDeEspacosViaFachada
from reservas.infrastructure.repositorio_com_agenda import RepositorioReservasComAgenda
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango


class ReservasDoEspacoViaCasoDeUso:
    def contar_ativas_fora_da_janela(
        self, espaco_id: int, abertura_em_minutos: int, fechamento_em_minutos: int
    ) -> int:
        caso_de_uso = ContarReservasAtivasForaDaJanela(
            RepositorioReservasDjango(), timezone.now
        )
        return caso_de_uso.executar(
            espaco_id, abertura_em_minutos, fechamento_em_minutos
        )


def agora() -> datetime:
    return timezone.now()


def _repositorio_com_agenda(
    relogio: Callable[[], datetime],
) -> RepositorioReservasComAgenda:
    return RepositorioReservasComAgenda(
        RepositorioReservasDjango(), AgendaDoDiaRedis(relogio)
    )


def criar_reserva(relogio: Callable[[], datetime] = timezone.now) -> CriarReserva:
    return CriarReserva(
        _repositorio_com_agenda(relogio), ConsultaDeEspacosViaFachada(), relogio
    )


def consultar_reservas() -> ConsultarReservas:
    return ConsultarReservas(RepositorioReservasDjango())


def obter_reserva() -> ObterReserva:
    return ObterReserva(RepositorioReservasDjango())


def alterar_situacao_reserva(
    relogio: Callable[[], datetime] = timezone.now,
) -> AlterarSituacaoReserva:
    return AlterarSituacaoReserva(_repositorio_com_agenda(relogio), relogio)


def consultar_historico_da_reserva() -> ConsultarHistoricoDaReserva:
    return ConsultarHistoricoDaReserva(RepositorioReservasDjango())


def reconstruir_agenda(
    relogio: Callable[[], datetime] = timezone.now,
) -> ReconstruirAgenda:
    return ReconstruirAgenda(
        RepositorioReservasDjango(), AgendaDoDiaRedis(relogio), relogio
    )


def consultar_ocupacao_do_dia(
    relogio: Callable[[], datetime] = timezone.now,
) -> ConsultarOcupacaoDoDia:
    return ConsultarOcupacaoDoDia(
        RepositorioReservasDjango(),
        ConsultaDeEspacosViaFachada(),
        AgendaDoDiaRedis(relogio),
        relogio,
    )
