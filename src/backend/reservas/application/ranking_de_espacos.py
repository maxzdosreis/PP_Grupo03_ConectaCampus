import logging
from dataclasses import dataclass

from reservas.application.fila_de_pendentes import exigir_gestor
from reservas.application.portas import (
    ConsultaDeEspacos,
    RankingDeEspacos,
    RankingIndisponivel,
)
from reservas.application.repositorio import RepositorioReservas
from reservas.domain.ator import Ator

logger = logging.getLogger(__name__)

LIMITE_MINIMO_DO_RANKING = 1
LIMITE_MAXIMO_DO_RANKING = 20
LIMITE_PADRAO_DO_RANKING = 5


@dataclass(frozen=True)
class PosicaoDoRanking:
    posicao: int
    espaco_id: int
    nome: str
    total: int


class ConsultarRankingDeEspacos:
    def __init__(
        self,
        repositorio: RepositorioReservas,
        ranking: RankingDeEspacos,
        consulta_de_espacos: ConsultaDeEspacos,
    ) -> None:
        self._repositorio = repositorio
        self._ranking = ranking
        self._consulta_de_espacos = consulta_de_espacos

    def executar(
        self, limite: int = LIMITE_PADRAO_DO_RANKING, *, ator: Ator
    ) -> tuple[PosicaoDoRanking, ...]:
        exigir_gestor(ator)
        pares = self._pela_projecao(limite)
        if pares is None:
            pares = self._repositorio.contar_por_espaco_que_contam_no_ranking(limite)
        return self._com_nomes(pares)

    def _pela_projecao(self, limite: int) -> tuple[tuple[int, int], ...] | None:
        try:
            return self._ranking.top(limite)
        except RankingIndisponivel:
            logger.warning("Ranking indisponível; ele sai do PostgreSQL.")
            return None

    def _com_nomes(
        self, pares: tuple[tuple[int, int], ...]
    ) -> tuple[PosicaoDoRanking, ...]:
        nomes = self._consulta_de_espacos.nomes_dos_espacos(
            [espaco_id for espaco_id, _ in pares]
        )
        return tuple(
            PosicaoDoRanking(
                posicao=posicao,
                espaco_id=espaco_id,
                nome=nomes.get(espaco_id, f"Espaço {espaco_id}"),
                total=total,
            )
            for posicao, (espaco_id, total) in enumerate(pares, start=1)
        )
