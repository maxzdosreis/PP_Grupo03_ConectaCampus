from collections.abc import Iterable
from datetime import datetime

from reservas.domain.excecoes import ConflitoDeHorario
from reservas.domain.reserva import Reserva


def garantir_horario_livre(nova: Reserva, existentes: Iterable[Reserva]) -> None:
    ocupante = min(
        (existente for existente in existentes if _ocupa_o_horario_de(nova, existente)),
        key=_inicio,
        default=None,
    )
    if ocupante is None:
        return
    raise ConflitoDeHorario(ocupante.intervalo, ocupante.situacao)


def _ocupa_o_horario_de(nova: Reserva, existente: Reserva) -> bool:
    return (
        _mesmo_espaco(nova, existente)
        and not _mesma_reserva(nova, existente)
        and existente.situacao.ocupa_horario
        and nova.intervalo.sobrepoe(existente.intervalo)
    )


def _mesmo_espaco(nova: Reserva, existente: Reserva) -> bool:
    return nova.espaco_id == existente.espaco_id


def _mesma_reserva(nova: Reserva, existente: Reserva) -> bool:
    return nova.id is not None and nova.id == existente.id


def _inicio(reserva: Reserva) -> datetime:
    return reserva.intervalo.inicio()
