import logging
from collections.abc import Callable, Sequence
from contextlib import AbstractContextManager
from datetime import date, datetime

from django.db import transaction

from reservas.application.portas import (
    AgendaDoDia,
    AgendaIndisponivel,
    IndiceDeReservas,
    IndiceIndisponivel,
    RankingDeEspacos,
    RankingIndisponivel,
    RegistroDoIndice,
    RegistroDoRanking,
)
from reservas.application.repositorio import (
    FiltrosDeReservas,
    Paginacao,
    PaginaDeReservas,
    RepositorioReservas,
)
from reservas.domain.registro_de_situacao import RegistroDeSituacao
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva

logger = logging.getLogger(__name__)

TENTATIVAS_DE_CONVERGENCIA = 3
AposOCommit = Callable[[Callable[[], None]], None]
Aplicacao = Callable[[Reserva], None]


def _apos_o_commit(acao: Callable[[], None]) -> None:
    transaction.on_commit(acao, robust=True)


class RepositorioReservasComAgenda(RepositorioReservas):
    def __init__(
        self,
        interno: RepositorioReservas,
        agenda: AgendaDoDia,
        indice: IndiceDeReservas,
        ranking: RankingDeEspacos,
        apos_o_commit: AposOCommit = _apos_o_commit,
    ) -> None:
        self._interno = interno
        self._agenda = agenda
        self._indice = indice
        self._ranking = ranking
        self._apos_o_commit = apos_o_commit

    def salvar(self, reserva: Reserva) -> Reserva:
        salva = self._interno.salvar(reserva)
        reserva_id = salva.id
        self._apos_o_commit(lambda: self._sincronizar(reserva_id))
        return salva

    def _sincronizar(self, reserva_id: int | None) -> None:
        if reserva_id is None:
            return
        self._sincronizar_projecao(
            reserva_id, self._aplicar_na_agenda, AgendaIndisponivel, "agenda"
        )
        self._sincronizar_projecao(
            reserva_id,
            self._aplicar_no_indice,
            IndiceIndisponivel,
            "índice de filas e contagens",
        )
        self._sincronizar_projecao(
            reserva_id,
            self._aplicar_no_ranking,
            RankingIndisponivel,
            "ranking de espaços",
        )

    def _sincronizar_projecao(
        self,
        reserva_id: int,
        aplicar: Aplicacao,
        indisponivel: type[Exception],
        nome: str,
    ) -> None:
        try:
            self._convergir(reserva_id, aplicar, nome)
        except indisponivel:
            logger.warning(
                "Redis não atualizado (%s) para a reserva %s; "
                "a reconstrução da agenda a refaz.",
                nome,
                reserva_id,
            )

    def _convergir(self, reserva_id: int, aplicar: Aplicacao, nome: str) -> None:
        aplicada = None
        for _ in range(TENTATIVAS_DE_CONVERGENCIA):
            atual = self._interno.obter_por_id(reserva_id)
            if atual is None or atual.situacao is aplicada:
                return
            aplicar(atual)
            aplicada = atual.situacao
        logger.warning(
            "A reserva %s continuou mudando durante a sincronização do Redis (%s); "
            "a reconstrução da agenda a refaz.",
            reserva_id,
            nome,
        )

    def _aplicar_na_agenda(self, reserva: Reserva) -> None:
        if reserva.situacao.ocupa_horario:
            self._agenda.registrar(
                reserva.espaco_id, reserva.id, reserva.intervalo, reserva.situacao
            )
        else:
            self._agenda.remover(reserva.espaco_id, reserva.id, reserva.intervalo.data)

    def _aplicar_no_indice(self, reserva: Reserva) -> None:
        self._indice.aplicar(reserva.id, reserva.situacao, reserva.criada_em)

    def _aplicar_no_ranking(self, reserva: Reserva) -> None:
        self._ranking.aplicar(reserva.id, reserva.espaco_id, reserva.situacao)

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

    def listar_pendentes(self, paginacao: Paginacao) -> PaginaDeReservas:
        return self._interno.listar_pendentes(paginacao)

    def listar_por_ids(self, ids: Sequence[int]) -> list[Reserva]:
        return self._interno.listar_por_ids(ids)

    def contar_por_situacao(self) -> dict[SituacaoReserva, int]:
        return self._interno.contar_por_situacao()

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

    def listar_para_indice(
        self, depois_de_id: int, limite: int
    ) -> list[RegistroDoIndice]:
        return self._interno.listar_para_indice(depois_de_id, limite)

    def contar_por_espaco_que_contam_no_ranking(
        self, limite: int
    ) -> tuple[tuple[int, int], ...]:
        return self._interno.contar_por_espaco_que_contam_no_ranking(limite)

    def listar_para_ranking(
        self, depois_de_id: int, limite: int
    ) -> list[RegistroDoRanking]:
        return self._interno.listar_para_ranking(depois_de_id, limite)
