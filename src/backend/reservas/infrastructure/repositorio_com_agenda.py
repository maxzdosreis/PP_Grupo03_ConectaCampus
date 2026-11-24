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
        atual = self._interno.obter_por_id(reserva_id)
        if atual is None:
            return
        try:
            if atual.situacao.ocupa_horario:
                self._agenda.registrar(
                    atual.espaco_id, reserva_id, atual.intervalo, atual.situacao
                )
            else:
                self._agenda.remover(atual.espaco_id, reserva_id, atual.intervalo.data)
        except AgendaIndisponivel:
            logger.warning(
                "Agenda do Redis não atualizada para a reserva %s; "
                "a reconstrução da agenda a refaz.",
                reserva_id,
            )

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

    def listar_ativas_a_partir_de(
        self, espaco_id: int, momento: datetime
    ) -> list[Reserva]:
        return self._interno.listar_ativas_a_partir_de(espaco_id, momento)

    def listar_historico(self, reserva_id: int) -> list[RegistroDeSituacao]:
        return self._interno.listar_historico(reserva_id)
