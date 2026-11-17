from dataclasses import dataclass
from datetime import time

from compartilhado.domain.erros import CampoObrigatorioAusente
from espacos.domain.excecoes import (
    HorarioDeFuncionamentoInvalido,
    JanelaDeFuncionamentoCurta,
)

MINUTOS_NO_DIA = 24 * 60
ABERTURA_PADRAO_EM_MINUTOS = 7 * 60
FECHAMENTO_PADRAO_EM_MINUTOS = MINUTOS_NO_DIA

JANELA_MINIMA_EM_MINUTOS = 30


@dataclass(frozen=True)
class HorarioDeFuncionamento:
    abertura_em_minutos: int
    fechamento_em_minutos: int

    def __post_init__(self) -> None:
        _exigir_minutos(self.abertura_em_minutos, "abertura")
        _exigir_minutos(self.fechamento_em_minutos, "fechamento")
        if self.abertura_em_minutos >= MINUTOS_NO_DIA:
            raise HorarioDeFuncionamentoInvalido("abertura")
        if self.fechamento_em_minutos <= self.abertura_em_minutos:
            raise HorarioDeFuncionamentoInvalido("fechamento")
        janela = self.fechamento_em_minutos - self.abertura_em_minutos
        if janela < JANELA_MINIMA_EM_MINUTOS:
            raise JanelaDeFuncionamentoCurta(JANELA_MINIMA_EM_MINUTOS)

    @classmethod
    def padrao(cls) -> "HorarioDeFuncionamento":
        return cls(ABERTURA_PADRAO_EM_MINUTOS, FECHAMENTO_PADRAO_EM_MINUTOS)

    @classmethod
    def de_horas(
        cls, abertura: time | None, fechamento: time | None
    ) -> "HorarioDeFuncionamento":
        if abertura is None:
            raise CampoObrigatorioAusente("abertura", "Abertura")
        if fechamento is None:
            raise CampoObrigatorioAusente("fechamento", "Fechamento")
        return cls(
            _minutos_da_hora(abertura, "abertura"),
            _minutos_do_fechamento(fechamento),
        )

    def abertura(self) -> time:
        return _hora_dos_minutos(self.abertura_em_minutos)

    def fechamento(self) -> time:
        return _hora_dos_minutos(self.fechamento_em_minutos)

    def com(
        self, *, abertura: time | None = None, fechamento: time | None = None
    ) -> "HorarioDeFuncionamento":
        return HorarioDeFuncionamento.de_horas(
            self.abertura() if abertura is None else abertura,
            self.fechamento() if fechamento is None else fechamento,
        )

    def __str__(self) -> str:
        return f"{self.abertura():%H:%M} às {self.fechamento():%H:%M}"


def _exigir_minutos(valor: int, campo: str) -> None:
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise HorarioDeFuncionamentoInvalido(campo)
    if not 0 <= valor <= MINUTOS_NO_DIA:
        raise HorarioDeFuncionamentoInvalido(campo)


def _minutos_da_hora(hora: time, campo: str) -> int:
    if not isinstance(hora, time):
        raise HorarioDeFuncionamentoInvalido(campo)
    return hora.hour * 60 + hora.minute


def _minutos_do_fechamento(hora: time) -> int:
    minutos = _minutos_da_hora(hora, "fechamento")
    return MINUTOS_NO_DIA if minutos == 0 else minutos


def _hora_dos_minutos(minutos: int) -> time:
    minutos %= MINUTOS_NO_DIA
    return time(minutos // 60, minutos % 60)
