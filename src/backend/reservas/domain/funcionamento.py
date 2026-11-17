from dataclasses import dataclass
from datetime import date, datetime, time, timedelta

from reservas.domain.intervalo_de_horario import FUSO_HORARIO, MEIA_NOITE

MINUTOS_NO_DIA = 24 * 60


@dataclass(frozen=True)
class FuncionamentoDoEspaco:
    abertura_em_minutos: int
    fechamento_em_minutos: int

    def __post_init__(self) -> None:
        if not 0 <= self.abertura_em_minutos < self.fechamento_em_minutos:
            raise ValueError("O funcionamento deve ter 0 <= abertura < fechamento.")
        if self.fechamento_em_minutos > MINUTOS_NO_DIA:
            raise ValueError("O fechamento não pode passar de 1440 minutos.")

    def abertura(self) -> time:
        return _hora_dos_minutos(self.abertura_em_minutos)

    def fechamento(self) -> time:
        return _hora_dos_minutos(self.fechamento_em_minutos)

    def abre_em(self, data: date) -> datetime:
        return _no_dia(data, self.abertura_em_minutos)

    def fecha_em(self, data: date) -> datetime:
        return _no_dia(data, self.fechamento_em_minutos)


def _no_dia(data: date, minutos: int) -> datetime:
    meia_noite = datetime.combine(data, MEIA_NOITE, tzinfo=FUSO_HORARIO)
    return meia_noite + timedelta(minutes=minutos)


def _hora_dos_minutos(minutos: int) -> time:
    minutos %= MINUTOS_NO_DIA
    return time(minutos // 60, minutos % 60)
