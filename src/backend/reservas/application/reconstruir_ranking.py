from collections.abc import Iterator
from dataclasses import dataclass

from reservas.application.portas import RankingDeEspacos, RegistroDoRanking
from reservas.application.repositorio import RepositorioReservas

TAMANHO_DO_LOTE = 500
TENTATIVAS_DE_RECONSTRUCAO = 3


@dataclass(frozen=True)
class ResultadoDaReconstrucaoDoRanking:
    espacos: int = 0
    reservas_contadas: int = 0
    descartado: bool = False


class ReconstruirRanking:
    def __init__(
        self, repositorio: RepositorioReservas, ranking: RankingDeEspacos
    ) -> None:
        self._repositorio = repositorio
        self._ranking = ranking

    def executar(self) -> ResultadoDaReconstrucaoDoRanking:
        for _ in range(TENTATIVAS_DE_RECONSTRUCAO):
            versao = self._ranking.versao()
            contagem = _Contagem()
            registros = contagem.contar(self._ler_do_banco())
            if self._ranking.substituir(registros, versao=versao):
                return ResultadoDaReconstrucaoDoRanking(
                    espacos=len(contagem.espacos),
                    reservas_contadas=contagem.reservas,
                )
        return ResultadoDaReconstrucaoDoRanking(descartado=True)

    def _ler_do_banco(self) -> Iterator[RegistroDoRanking]:
        ultimo_id = 0
        while lote := self._repositorio.listar_para_ranking(ultimo_id, TAMANHO_DO_LOTE):
            yield from lote
            ultimo_id = lote[-1].reserva_id


class _Contagem:
    def __init__(self) -> None:
        self.reservas = 0
        self.espacos: set[int] = set()

    def contar(
        self, registros: Iterator[RegistroDoRanking]
    ) -> Iterator[RegistroDoRanking]:
        for registro in registros:
            if registro.situacao.conta_no_ranking:
                self.reservas += 1
                self.espacos.add(registro.espaco_id)
            yield registro
