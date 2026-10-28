from enum import StrEnum

from reservas.domain.ator import PapelDoAtor


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
    def rotulo_da_acao(self) -> str:
        return _ROTULOS_DAS_ACOES[self]

    @property
    def eh_final(self) -> bool:
        return not TRANSICOES_PERMITIDAS[self]

    @property
    def ocupa_horario(self) -> bool:
        return self in SITUACOES_QUE_OCUPAM_HORARIO


_ROTULOS = {
    SituacaoReserva.SOLICITADA: "Solicitada",
    SituacaoReserva.CONFIRMADA: "Confirmada",
    SituacaoReserva.RECUSADA: "Recusada",
    SituacaoReserva.CANCELADA: "Cancelada",
    SituacaoReserva.CONCLUIDA: "Concluída",
}

_ROTULOS_DAS_ACOES = {
    SituacaoReserva.CONFIRMADA: "Confirmar",
    SituacaoReserva.RECUSADA: "Recusar",
    SituacaoReserva.CANCELADA: "Cancelar",
    SituacaoReserva.CONCLUIDA: "Concluir",
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

DESTINOS_DE_TRANSICAO = frozenset().union(*TRANSICOES_PERMITIDAS.values())

DESTINOS_POR_PAPEL: dict[PapelDoAtor, frozenset[SituacaoReserva]] = {
    PapelDoAtor.GESTOR: frozenset(
        {
            SituacaoReserva.CONFIRMADA,
            SituacaoReserva.RECUSADA,
            SituacaoReserva.CONCLUIDA,
            SituacaoReserva.CANCELADA,
        }
    ),
    PapelDoAtor.SOLICITANTE: frozenset({SituacaoReserva.CANCELADA}),
}

SITUACOES_QUE_EXIGEM_MOTIVO = frozenset(
    {SituacaoReserva.RECUSADA, SituacaoReserva.CANCELADA}
)

SITUACOES_QUE_OCUPAM_HORARIO = frozenset(
    {SituacaoReserva.SOLICITADA, SituacaoReserva.CONFIRMADA}
)


def transicao_permitida(atual: SituacaoReserva, nova: SituacaoReserva) -> bool:
    return nova in TRANSICOES_PERMITIDAS[atual]


def transicoes_a_partir_de(situacao: SituacaoReserva) -> list[SituacaoReserva]:
    return [nova for nova in SituacaoReserva if transicao_permitida(situacao, nova)]


def papel_pode_levar_a(papel: PapelDoAtor, nova: SituacaoReserva) -> bool:
    return nova in DESTINOS_POR_PAPEL[papel]
