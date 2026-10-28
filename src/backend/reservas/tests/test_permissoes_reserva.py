from datetime import date, datetime, time
from itertools import product
from zoneinfo import ZoneInfo

import pytest

from compartilhado.api.tratador_de_erros import tratar_excecao
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.excecoes import (
    AlteracaoDeSituacaoNaoPermitida,
    ReservaNaoEncontrada,
    TransicaoDeSituacaoInvalida,
)
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import DESTINOS_POR_PAPEL, SituacaoReserva
from reservas.domain.solicitante import Solicitante

S = SituacaoReserva
P = PapelDoAtor
SAO_PAULO = ZoneInfo("America/Sao_Paulo")
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=SAO_PAULO)
DONA_ID = 7
OUTRO_ID = 8
MOTIVO = "Chuva forte"
ANA = Solicitante(usuario_id=DONA_ID, nome="Ana Souza", matricula="2026001")

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
        usuario_id=DONA_ID if dono else OUTRO_ID,
        nome="Solicitante de Teste",
        papel=papel,
    )


def _reserva_em(situacao):
    return Reserva(
        id=12,
        espaco_id=3,
        solicitante=ANA,
        intervalo=IntervaloDeHorario(
            data=date(2026, 10, 25), hora_inicio=time(10, 0), hora_fim=time(11, 0)
        ),
        finalidade="Treino",
        situacao=situacao,
        motivo_da_situacao=MOTIVO if situacao in (S.RECUSADA, S.CANCELADA) else None,
        criada_em=AGORA,
    )


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
    assert reserva.situacao is S.SOLICITADA


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
def test_visivel_para(papel, dono, visivel):
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
