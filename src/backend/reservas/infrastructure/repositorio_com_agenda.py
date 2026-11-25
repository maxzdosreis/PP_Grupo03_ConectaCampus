import logging
from collections.abc import Callable
from contextlib import AbstractContextManager
from datetime import date, datetime

from django.db import transaction

from reservas.application.portas import AgendaDoDia, AgendaIndisponivel
from reservas.application.repositorio import (
    FiltrosDeReservas,
    Paginacao,
    PaginaDeReservas,
    RepositorioReservas,
)
from reservas.domain.registro_de_situacao import RegistroDeSituacao
from reservas.domain.reserva import Reserva

logger = logging.getLogger(__name__)

TENTATIVAS_DE_CONVERGENCIA = 3
AposOCommit = Callable[[Callable[[], None]], None]


def _apos_o_commit(acao: Callable[[], None]) -> None:
    transaction.on_commit(acao, robust=True)


class RepositorioReservasComAgenda(RepositorioReservas):
    def __init__(
        self,
        interno: RepositorioReservas,
        agenda: AgendaDoDia,
        apos_o_commit: AposOCommit = _apos_o_commit,
    ) -> None:
        self._interno = interno
        self._agenda = agenda
        self._apos_o_commit = apos_o_commit

    def salvar(self, reserva: Reserva) -> Reserva:
        salva = self._interno.salvar(reserva)
        reserva_id = salva.id
        self._apos_o_commit(lambda: self._sincronizar(reserva_id))
        return salva

    def _sincronizar(self, reserva_id: int | None) -> None:
        if reserva_id is None:
            return
        try:
            self._convergir(reserva_id)
        except AgendaIndisponivel:
            logger.warning(
                "Agenda do Redis não atualizada para a reserva %s; "
                "a reconstrução da agenda a refaz.",
                reserva_id,
            )

    def _convergir(self, reserva_id: int) -> None:
        aplicada = None
        for _ in range(TENTATIVAS_DE_CONVERGENCIA):
            atual = self._interno.obter_por_id(reserva_id)
            if atual is None or atual.situacao is aplicada:
                return
            self._aplicar(atual)
            aplicada = atual.situacao
        logger.warning(
            "A reserva %s continuou mudando durante a sincronização da agenda; "
            "a reconstrução da agenda a refaz.",
            reserva_id,
        )

    def _aplicar(self, reserva: Reserva) -> None:
        if reserva.situacao.ocupa_horario:
            self._agenda.registrar(
                reserva.espaco_id, reserva.id, reserva.intervalo, reserva.situacao
            )
        else:
            self._agenda.remover(reserva.espaco_id, reserva.id, reserva.intervalo.data)

    def em_transacao(self) -> AbstractContextManager[None]:
        return self._interno.em_transacao()

    def gravar_tentativa_recusada(
        self, reserva_id: int, registro: RegistroDeSituacao
    ) -> None:
        self._interno.gravar_tentativa_recusada(reserva_id, registro)

    def obter_por_id(self, reserva_id: int) -> Reserva | None:
        return self._interno.obter_por_id(reserva_id)

    def listar(
        self, filtros: FiltrosDeReservas, paginacao: Paginacao
    ) -> PaginaDeReservas:
        return self._interno.listar(filtros, paginacao)

    def listar_que_ocupam_horario(self, espaco_id: int, data: date) -> list[Reserva]:
        return self._interno.listar_que_ocupam_horario(espaco_id, data)

    def listar_dias_com_reservas_que_ocupam_horario(
        self, a_partir_de: date
    ) -> list[tuple[int, date]]:
        return self._interno.listar_dias_com_reservas_que_ocupam_horario(a_partir_de)

    def listar_ativas_a_partir_de(
        self, espaco_id: int, momento: datetime
    ) -> list[Reserva]:
        return self._interno.listar_ativas_a_partir_de(espaco_id, momento)

    def listar_historico(self, reserva_id: int) -> list[RegistroDeSituacao]:
        return self._interno.listar_historico(reserva_id)
