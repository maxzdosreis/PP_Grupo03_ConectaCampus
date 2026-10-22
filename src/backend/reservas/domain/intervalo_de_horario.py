from dataclasses import dataclass
from datetime import date, datetime, time
from zoneinfo import ZoneInfo

from compartilhado.domain.erros import CampoObrigatorioAusente
from reservas.domain.excecoes import HorarioInvalido

FUSO_HORARIO = ZoneInfo("America/Sao_Paulo")


@dataclass(frozen=True)
class IntervaloDeHorario:
    data: date
    hora_inicio: time
    hora_fim: time

    def __post_init__(self) -> None:
        _validar_data(self.data)
        _validar_hora(self.hora_inicio, "hora_inicio", "Hora de início")
        _validar_hora(self.hora_fim, "hora_fim", "Hora de término")
        if self.hora_fim <= self.hora_inicio:
            raise HorarioInvalido()

    def inicio(self) -> datetime:
        return datetime.combine(self.data, self.hora_inicio, tzinfo=FUSO_HORARIO)

    def fim(self) -> datetime:
        return datetime.combine(self.data, self.hora_fim, tzinfo=FUSO_HORARIO)

    def __str__(self) -> str:
        return f"{self.data:%d/%m/%Y} {self.hora_inicio:%H:%M}–{self.hora_fim:%H:%M}"


def _validar_data(data: date | None) -> None:
    if data is None:
        raise CampoObrigatorioAusente("data", "Data")
    if isinstance(data, datetime) or not isinstance(data, date):
        raise TypeError("data deve ser um date, não um datetime.")


def _validar_hora(hora: time | None, campo: str, rotulo: str) -> None:
    if hora is None:
        raise CampoObrigatorioAusente(campo, rotulo)
    if not isinstance(hora, time):
        raise TypeError(f"{campo} deve ser um time.")
