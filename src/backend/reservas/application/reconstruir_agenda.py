from collections.abc import Callable
from dataclasses import dataclass
from datetime import date, datetime

from reservas.application.ocupacao_do_dia import HorarioOcupado, ocupados_por_reserva
from reservas.application.portas import AgendaDoDia
from reservas.application.repositorio import RepositorioReservas
from reservas.domain.intervalo_de_horario import FUSO_HORARIO

TENTATIVAS_POR_DIA = 3


@dataclass(frozen=True)
class ResultadoDaReconstrucao:
    dias_refeitos: int = 0
    reservas_gravadas: int = 0
    dias_esvaziados: int = 0
    dias_descartados: int = 0


class ReconstruirAgenda:
    def __init__(
        self,
        repositorio: RepositorioReservas,
        agenda: AgendaDoDia,
        relogio: Callable[[], datetime],
    ) -> None:
        self._repositorio = repositorio
        self._agenda = agenda
        self._relogio = relogio

    def executar(self) -> ResultadoDaReconstrucao:
        hoje = self._relogio().astimezone(FUSO_HORARIO).date()
        projetados = self._agenda.dias_projetados(hoje)
        do_banco = self._repositorio.listar_dias_com_reservas_que_ocupam_horario(hoje)
        resultado = ResultadoDaReconstrucao()
        for espaco_id, data in sorted(projetados.union(do_banco)):
            resultado = _somar(
                resultado,
                self._refazer_o_dia(
                    espaco_id, data, estava_projetado=(espaco_id, data) in projetados
                ),
            )
        return resultado

    def _refazer_o_dia(
        self, espaco_id: int, data: date, *, estava_projetado: bool
    ) -> ResultadoDaReconstrucao:
        for _ in range(TENTATIVAS_POR_DIA):
            versao = self._agenda.versao(espaco_id, data)
            reservas = self._repositorio.listar_que_ocupam_horario(espaco_id, data)
            ocupados = ocupados_por_reserva(reservas)
            if not self._retrato_continua_atual(espaco_id, data, ocupados):
                continue
            esvaziado = (
                estava_projetado
                and not ocupados
                and bool(self._agenda.listar(espaco_id, data))
            )
            if self._agenda.substituir(espaco_id, data, ocupados, versao=versao):
                return ResultadoDaReconstrucao(
                    dias_refeitos=1,
                    reservas_gravadas=len(ocupados),
                    dias_esvaziados=int(esvaziado),
                )
        return ResultadoDaReconstrucao(dias_descartados=1)

    def _retrato_continua_atual(
        self, espaco_id: int, data: date, ocupados: dict[int, HorarioOcupado]
    ) -> bool:
        reservas = self._repositorio.listar_que_ocupam_horario(espaco_id, data)
        return ocupados_por_reserva(reservas) == ocupados


def _somar(
    total: ResultadoDaReconstrucao, dia: ResultadoDaReconstrucao
) -> ResultadoDaReconstrucao:
    return ResultadoDaReconstrucao(
        dias_refeitos=total.dias_refeitos + dia.dias_refeitos,
        reservas_gravadas=total.reservas_gravadas + dia.reservas_gravadas,
        dias_esvaziados=total.dias_esvaziados + dia.dias_esvaziados,
        dias_descartados=total.dias_descartados + dia.dias_descartados,
    )
