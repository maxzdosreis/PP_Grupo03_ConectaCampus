from collections.abc import Callable
from datetime import datetime

from django.utils import timezone

from reservas.application.casos_de_uso import (
    AlterarSituacaoReserva,
    ConsultarHistoricoDaReserva,
    ConsultarOcupacaoDoDia,
    ConsultarReservas,
    CriarReserva,
    ObterReserva,
)
from reservas.infrastructure.consulta_de_espacos import ConsultaDeEspacosViaFachada
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango


def criar_reserva(relogio: Callable[[], datetime] = timezone.now) -> CriarReserva:
    return CriarReserva(
        RepositorioReservasDjango(), ConsultaDeEspacosViaFachada(), relogio
    )


def consultar_reservas() -> ConsultarReservas:
    return ConsultarReservas(RepositorioReservasDjango())


def obter_reserva() -> ObterReserva:
    return ObterReserva(RepositorioReservasDjango())


def alterar_situacao_reserva(
    relogio: Callable[[], datetime] = timezone.now,
) -> AlterarSituacaoReserva:
    return AlterarSituacaoReserva(RepositorioReservasDjango(), relogio)


def consultar_historico_da_reserva() -> ConsultarHistoricoDaReserva:
    return ConsultarHistoricoDaReserva(RepositorioReservasDjango())


def consultar_ocupacao_do_dia(
    relogio: Callable[[], datetime] = timezone.now,
) -> ConsultarOcupacaoDoDia:
    return ConsultarOcupacaoDoDia(
        RepositorioReservasDjango(), ConsultaDeEspacosViaFachada(), relogio
    )
