from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from compartilhado.domain.erros import CampoObrigatorioAusente
from reservas.domain.excecoes import HorarioInvalido

FUSO_HORARIO = ZoneInfo("America/Sao_Paulo")
MEIA_NOITE = time(0, 0)


@dataclass(frozen=True)
class IntervaloDeHorario:
    data: date
    hora_inicio: time
    hora_fim: time

    def __post_init__(self) -> None:
        _validar_data(self.data)
        _validar_hora(self.hora_inicio, "hora_inicio", "Hora de início")
        _validar_hora(self.hora_fim, "hora_fim", "Hora de término")
        if self._termina_antes_de_comecar():
            raise HorarioInvalido()

    def inicio(self) -> datetime:
        return datetime.combine(self.data, self.hora_inicio, tzinfo=FUSO_HORARIO)

    def fim(self) -> datetime:
        return datetime.combine(self._data_do_fim(), self.hora_fim, tzinfo=FUSO_HORARIO)

    def termina_a_meia_noite(self) -> bool:
        return self.hora_fim == MEIA_NOITE

    def _termina_antes_de_comecar(self) -> bool:
        if self.termina_a_meia_noite():
            return False
        return self.hora_fim <= self.hora_inicio

    def _data_do_fim(self) -> date:
        if self.termina_a_meia_noite():
            return self.data + timedelta(days=1)
        return self.data

    def sobrepoe(self, outro: "IntervaloDeHorario") -> bool:
        return self.inicio() < outro.fim() and outro.inicio() < self.fim()

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
