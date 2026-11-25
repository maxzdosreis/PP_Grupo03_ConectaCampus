import logging

from compartilhado.domain.erros import AcaoNaoPermitida
from reservas.application.portas import IndiceDeReservas, IndiceIndisponivel
from reservas.application.repositorio import (
    Paginacao,
    PaginaDeReservas,
    RepositorioReservas,
)
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.situacao import SituacaoReserva

logger = logging.getLogger(__name__)


class ConsultarFilaDePendentes:
    def __init__(
        self, repositorio: RepositorioReservas, indice: IndiceDeReservas
    ) -> None:
        self._repositorio = repositorio
        self._indice = indice

    def executar(self, paginacao: Paginacao, *, ator: Ator) -> PaginaDeReservas:
        _exigir_gestor(ator)
        pagina = self._pelo_indice(paginacao)
        if pagina is None:
            return self._repositorio.listar_pendentes(paginacao)
        return pagina

    def _pelo_indice(self, paginacao: Paginacao) -> PaginaDeReservas | None:
        try:
            ids = self._indice.pendentes(paginacao.tamanho, paginacao.deslocamento())
            contagem = self._indice.contagem_por_situacao()
        except IndiceIndisponivel:
            logger.warning("Índice indisponível; a fila sai do PostgreSQL.")
            return None
        if ids is None or contagem is None:
            return None
        reservas = self._repositorio.listar_por_ids(ids)
        pendentes = tuple(
            reserva
            for reserva in reservas
            if reserva.situacao is SituacaoReserva.SOLICITADA
        )
        return PaginaDeReservas(
            itens=pendentes,
            total=contagem[SituacaoReserva.SOLICITADA],
            paginacao=paginacao,
        )


class ContarReservasPorSituacao:
    def __init__(
        self, repositorio: RepositorioReservas, indice: IndiceDeReservas
    ) -> None:
        self._repositorio = repositorio
        self._indice = indice

    def executar(self, *, ator: Ator) -> dict[SituacaoReserva, int]:
        _exigir_gestor(ator)
        contagem = self._pelo_indice()
        if contagem is None:
            return self._repositorio.contar_por_situacao()
        return contagem

    def _pelo_indice(self) -> dict[SituacaoReserva, int] | None:
        try:
            return self._indice.contagem_por_situacao()
        except IndiceIndisponivel:
            logger.warning("Índice indisponível; a contagem sai do PostgreSQL.")
            return None


def _exigir_gestor(ator: Ator) -> None:
    if ator.papel is not PapelDoAtor.GESTOR:
        raise AcaoNaoPermitida
