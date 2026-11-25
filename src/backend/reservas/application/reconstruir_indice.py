from collections.abc import Iterator
from dataclasses import dataclass

from reservas.application.portas import IndiceDeReservas, RegistroDoIndice
from reservas.application.repositorio import RepositorioReservas
from reservas.domain.situacao import SituacaoReserva

TAMANHO_DO_LOTE = 500
TENTATIVAS_DE_RECONSTRUCAO = 3


@dataclass(frozen=True)
class ResultadoDaReconstrucaoDoIndice:
    reservas_indexadas: int = 0
    pendentes: int = 0
    descartado: bool = False


class ReconstruirIndice:
    def __init__(
        self, repositorio: RepositorioReservas, indice: IndiceDeReservas
    ) -> None:
        self._repositorio = repositorio
        self._indice = indice

    def executar(self) -> ResultadoDaReconstrucaoDoIndice:
        for _ in range(TENTATIVAS_DE_RECONSTRUCAO):
            versao = self._indice.versao()
            contagem = _Contagem()
            registros = contagem.contar(self._ler_do_banco())
            if self._indice.substituir(registros, versao=versao):
                return ResultadoDaReconstrucaoDoIndice(
                    reservas_indexadas=contagem.reservas, pendentes=contagem.pendentes
                )
        return ResultadoDaReconstrucaoDoIndice(descartado=True)

    def _ler_do_banco(self) -> Iterator[RegistroDoIndice]:
        ultimo_id = 0
        while lote := self._repositorio.listar_para_indice(ultimo_id, TAMANHO_DO_LOTE):
            yield from lote
            ultimo_id = lote[-1].reserva_id


class _Contagem:
    def __init__(self) -> None:
        self.reservas = 0
        self.pendentes = 0

    def contar(
        self, registros: Iterator[RegistroDoIndice]
    ) -> Iterator[RegistroDoIndice]:
        for registro in registros:
            self.reservas += 1
            self.pendentes += registro.situacao is SituacaoReserva.SOLICITADA
            yield registro
