from enum import StrEnum


class SituacaoReserva(StrEnum):
    SOLICITADA = "SOLICITADA"
    CONFIRMADA = "CONFIRMADA"
    RECUSADA = "RECUSADA"
    CANCELADA = "CANCELADA"
    CONCLUIDA = "CONCLUIDA"

    @property
    def rotulo(self) -> str:
        return _ROTULOS[self]

    @property
    def eh_final(self) -> bool:
        return not TRANSICOES_PERMITIDAS[self]


_ROTULOS = {
    SituacaoReserva.SOLICITADA: "Solicitada",
    SituacaoReserva.CONFIRMADA: "Confirmada",
    SituacaoReserva.RECUSADA: "Recusada",
    SituacaoReserva.CANCELADA: "Cancelada",
    SituacaoReserva.CONCLUIDA: "Concluída",
}

TRANSICOES_PERMITIDAS: dict[SituacaoReserva, frozenset[SituacaoReserva]] = {
    SituacaoReserva.SOLICITADA: frozenset(
        {
            SituacaoReserva.CONFIRMADA,
            SituacaoReserva.RECUSADA,
            SituacaoReserva.CANCELADA,
        }
    ),
    SituacaoReserva.CONFIRMADA: frozenset(
        {SituacaoReserva.CONCLUIDA, SituacaoReserva.CANCELADA}
    ),
    SituacaoReserva.CONCLUIDA: frozenset(),
    SituacaoReserva.RECUSADA: frozenset(),
    SituacaoReserva.CANCELADA: frozenset(),
}

SITUACOES_QUE_EXIGEM_MOTIVO = frozenset(
    {SituacaoReserva.RECUSADA, SituacaoReserva.CANCELADA}
)


def transicao_permitida(atual: SituacaoReserva, nova: SituacaoReserva) -> bool:
    return nova in TRANSICOES_PERMITIDAS[atual]
