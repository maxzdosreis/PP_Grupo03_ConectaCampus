from itertools import product

import pytest

from compartilhado.api.tratador_de_erros import tratar_excecao
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.excecoes import (
    AlteracaoDeSituacaoNaoPermitida,
    ReservaNaoEncontrada,
    TransicaoDeSituacaoInvalida,
)
from reservas.domain.situacao import DESTINOS_POR_PAPEL, SituacaoReserva
from reservas.tests.fakes import AGORA, ANA, BRUNO, MOTIVO, reserva_reconstituida

S = SituacaoReserva
P = PapelDoAtor

TABELA_DE_PERMISSOES = {
    P.GESTOR: {S.CONFIRMADA, S.RECUSADA, S.CONCLUIDA, S.CANCELADA},
    P.SOLICITANTE: {S.CANCELADA},
}
TRANSICOES = {
    (S.SOLICITADA, S.CONFIRMADA),
    (S.SOLICITADA, S.RECUSADA),
    (S.SOLICITADA, S.CANCELADA),
    (S.CONFIRMADA, S.CONCLUIDA),
    (S.CONFIRMADA, S.CANCELADA),
}
DESTINOS_ALCANCAVEIS = {nova for _, nova in TRANSICOES}

SUCESSO = "sucesso"
PROIBIDA = "403"
TRANSICAO_INVALIDA = "409"
NAO_VISIVEL = "nao_visivel"

_EXCECAO_ESPERADA = {
    PROIBIDA: AlteracaoDeSituacaoNaoPermitida,
    TRANSICAO_INVALIDA: TransicaoDeSituacaoInvalida,
    NAO_VISIVEL: ReservaNaoEncontrada,
}


def _resultado_esperado(papel, atual, nova, dono):
    if papel is P.SOLICITANTE and not dono:
        return NAO_VISIVEL
    if nova in DESTINOS_ALCANCAVEIS and nova not in TABELA_DE_PERMISSOES[papel]:
        return PROIBIDA
    if (atual, nova) not in TRANSICOES:
        return TRANSICAO_INVALIDA
    return SUCESSO


MATRIZ = [
    (papel, atual, nova, dono, _resultado_esperado(papel, atual, nova, dono))
    for papel, atual, nova, dono in product(P, S, S, [True, False])
]


def _id_do_caso(caso):
    papel, atual, nova, dono, esperado = caso
    quem = "dono" if dono else "outro"
    return f"{papel}-{quem}-{atual}->{nova}-{esperado}"


def _ator(papel, dono):
    return Ator(
        usuario_id=ANA.usuario_id if dono else BRUNO.usuario_id,
        nome="Solicitante de Teste",
        papel=papel,
    )


def _reserva_em(situacao):
    return reserva_reconstituida(situacao=situacao)


def _retrato(reserva):
    return reserva.situacao, reserva.motivo_da_situacao, reserva.registros_pendentes


def test_destinos_por_papel_sao_os_da_tabela_do_claude_md():
    # Arrange
    tabela = dict(DESTINOS_POR_PAPEL)

    # Assert
    assert tabela == {
        P.GESTOR: frozenset({S.CONFIRMADA, S.RECUSADA, S.CONCLUIDA, S.CANCELADA}),
        P.SOLICITANTE: frozenset({S.CANCELADA}),
    }


@pytest.mark.parametrize(
    ("papel", "atual", "nova", "dono", "esperado"), MATRIZ, ids=map(_id_do_caso, MATRIZ)
)
def test_acoes_permitidas_contem_o_destino_so_quando_a_alteracao_e_aceita(
    papel, atual, nova, dono, esperado
):
    # Act
    acoes = _reserva_em(atual).acoes_permitidas_para(_ator(papel, dono))

    # Assert
    assert (nova in acoes) is (esperado == SUCESSO)


@pytest.mark.parametrize(
    ("papel", "atual", "nova", "dono", "esperado"), MATRIZ, ids=map(_id_do_caso, MATRIZ)
)
def test_alterar_situacao_segue_a_matriz_e_preserva_a_reserva_nos_erros(
    papel, atual, nova, dono, esperado
):
    # Arrange
    reserva = _reserva_em(atual)
    antes = _retrato(reserva)

    # Act / Assert
    if esperado == SUCESSO:
        reserva.alterar_situacao(
            nova, motivo=MOTIVO, ator=_ator(papel, dono), agora=AGORA
        )
        assert reserva.situacao is nova
        assert len(reserva.registros_pendentes) == 1
        return
    with pytest.raises(_EXCECAO_ESPERADA[esperado]):
        reserva.alterar_situacao(
            nova, motivo=MOTIVO, ator=_ator(papel, dono), agora=AGORA
        )
    assert _retrato(reserva) == antes


@pytest.mark.parametrize(
    ("atual", "esperadas"),
    [
        (S.SOLICITADA, [S.CONFIRMADA, S.RECUSADA, S.CANCELADA]),
        (S.CONFIRMADA, [S.CANCELADA, S.CONCLUIDA]),
        (S.CONCLUIDA, []),
    ],
)
def test_acoes_do_gestor_seguem_a_ordem_do_enum(atual, esperadas):
    # Act
    acoes = _reserva_em(atual).acoes_permitidas_para(_ator(P.GESTOR, dono=False))

    # Assert
    assert acoes == esperadas


@pytest.mark.parametrize(
    ("atual", "esperadas"),
    [
        (S.SOLICITADA, [S.CANCELADA]),
        (S.CONFIRMADA, [S.CANCELADA]),
        (S.CONCLUIDA, []),
    ],
)
def test_acoes_do_solicitante_na_propria_sao_so_cancelar(atual, esperadas):
    # Act
    acoes = _reserva_em(atual).acoes_permitidas_para(_ator(P.SOLICITANTE, dono=True))

    # Assert
    assert acoes == esperadas


def test_solicitante_concluindo_uma_solicitada_recebe_403_e_nao_409():
    # Arrange
    reserva = _reserva_em(S.SOLICITADA)

    # Act / Assert
    with pytest.raises(AlteracaoDeSituacaoNaoPermitida) as erro:
        reserva.alterar_situacao(
            S.CONCLUIDA, ator=_ator(P.SOLICITANTE, dono=True), agora=AGORA
        )

    assert erro.value.mensagem == "Somente o gestor pode concluir reservas."
    assert erro.value.nova is S.CONCLUIDA
    assert reserva.situacao is S.SOLICITADA


def test_quem_nao_ve_a_reserva_recebe_nao_encontrada_com_o_codigo_dela():
    # Arrange
    reserva = _reserva_em(S.SOLICITADA)

    # Act
    with pytest.raises(ReservaNaoEncontrada) as erro:
        reserva.alterar_situacao(
            S.CANCELADA,
            motivo=MOTIVO,
            ator=_ator(P.SOLICITANTE, dono=False),
            agora=AGORA,
        )

    # Assert
    assert erro.value.reserva_id == reserva.id


@pytest.mark.parametrize("papel", P)
def test_solicitada_como_destino_e_transicao_invalida_para_os_dois_papeis(papel):
    # Arrange
    reserva = _reserva_em(S.CONFIRMADA)

    # Act / Assert
    with pytest.raises(TransicaoDeSituacaoInvalida):
        reserva.alterar_situacao(
            S.SOLICITADA, ator=_ator(papel, dono=True), agora=AGORA
        )


@pytest.mark.parametrize(
    ("papel", "dono", "visivel"),
    [
        (P.GESTOR, True, True),
        (P.GESTOR, False, True),
        (P.SOLICITANTE, True, True),
        (P.SOLICITANTE, False, False),
    ],
)
def test_so_o_gestor_e_o_dono_enxergam_a_reserva(papel, dono, visivel):
    # Assert
    assert _reserva_em(S.SOLICITADA).visivel_para(_ator(papel, dono)) is visivel


def test_alteracao_nao_permitida_vira_403_com_acao_nao_permitida():
    # Act
    resposta = tratar_excecao(AlteracaoDeSituacaoNaoPermitida(S.CONFIRMADA), {})

    # Assert
    assert resposta.status_code == 403
    assert resposta.data == {
        "erro": {
            "codigo": "ACAO_NAO_PERMITIDA",
            "mensagem": "Somente o gestor pode confirmar reservas.",
        }
    }
