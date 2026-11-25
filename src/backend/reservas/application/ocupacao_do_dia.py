from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date, time

from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva


@dataclass(frozen=True)
class HorarioOcupado:
    intervalo: IntervaloDeHorario
    situacao: SituacaoReserva


@dataclass(frozen=True)
class OcupacaoDoDia:
    data: date
    horario_de_abertura: time
    horario_de_fechamento: time
    ocupados: tuple[HorarioOcupado, ...]
    livres: tuple[IntervaloDeHorario, ...]
    reservavel: bool
    motivo_indisponivel: str | None


def ocupados_por_reserva(reservas: Iterable[Reserva]) -> dict[int, HorarioOcupado]:
    return {
        reserva.id: _ao_minuto(reserva.intervalo, reserva.situacao)
        for reserva in reservas
    }


def _ao_minuto(
    intervalo: IntervaloDeHorario, situacao: SituacaoReserva
) -> HorarioOcupado:
    return HorarioOcupado(
        intervalo=IntervaloDeHorario(
            data=intervalo.data,
            hora_inicio=intervalo.hora_inicio.replace(second=0, microsecond=0),
            hora_fim=intervalo.hora_fim.replace(second=0, microsecond=0),
        ),
        situacao=situacao,
    )
