from dataclasses import dataclass
from datetime import date, time

from reservas.domain.intervalo_de_horario import IntervaloDeHorario
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
