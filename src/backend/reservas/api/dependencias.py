from django.utils import timezone

from reservas.application.casos_de_uso import (
    ConsultarReservas,
    CriarReserva,
    ObterReserva,
)
from reservas.infrastructure.consulta_de_espacos import ConsultaDeEspacosViaFachada
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango


def criar_reserva() -> CriarReserva:
    return CriarReserva(
        RepositorioReservasDjango(), ConsultaDeEspacosViaFachada(), timezone.now
    )


def consultar_reservas() -> ConsultarReservas:
    return ConsultarReservas(RepositorioReservasDjango())


def obter_reserva() -> ObterReserva:
    return ObterReserva(RepositorioReservasDjango())
