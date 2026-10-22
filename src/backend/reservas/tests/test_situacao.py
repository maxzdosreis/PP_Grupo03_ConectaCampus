import itertools

import pytest

from reservas.domain.situacao import (
    SITUACOES_QUE_EXIGEM_MOTIVO,
    SITUACOES_QUE_OCUPAM_HORARIO,
    SituacaoReserva,
    transicao_permitida,
)

S = SituacaoReserva

TABELA = {
    (S.SOLICITADA, S.CONFIRMADA),
    (S.SOLICITADA, S.RECUSADA),
    (S.SOLICITADA, S.CANCELADA),
    (S.CONFIRMADA, S.CONCLUIDA),
    (S.CONFIRMADA, S.CANCELADA),
}

TODOS_OS_PARES = list(itertools.product(SituacaoReserva, repeat=2))


def test_ha_25_pares_de_situacoes():
    # Assert
    assert len(TODOS_OS_PARES) == 25


@pytest.mark.parametrize(("atual", "nova"), TODOS_OS_PARES)
def test_transicao_permitida_segue_a_tabela(atual, nova):
    # Act
    permitida = transicao_permitida(atual, nova)

    # Assert
    assert permitida is ((atual, nova) in TABELA)


@pytest.mark.parametrize("situacao", [S.CONCLUIDA, S.RECUSADA, S.CANCELADA])
def test_estados_finais_nao_tem_saida(situacao):
    # Assert
    assert situacao.eh_final is True


@pytest.mark.parametrize("situacao", [S.SOLICITADA, S.CONFIRMADA])
def test_estados_intermediarios_nao_sao_finais(situacao):
    # Assert
    assert situacao.eh_final is False


@pytest.mark.parametrize(
    ("situacao", "rotulo"),
    [
        (S.SOLICITADA, "Solicitada"),
        (S.CONFIRMADA, "Confirmada"),
        (S.RECUSADA, "Recusada"),
        (S.CANCELADA, "Cancelada"),
        (S.CONCLUIDA, "Concluída"),
    ],
)
def test_rotulo_em_portugues(situacao, rotulo):
    # Assert
    assert situacao.rotulo == rotulo


def test_recusar_e_cancelar_exigem_motivo():
    # Assert
    assert frozenset({S.RECUSADA, S.CANCELADA}) == SITUACOES_QUE_EXIGEM_MOTIVO


def test_solicitada_e_confirmada_ocupam_horario():
    # Assert
    assert frozenset({S.SOLICITADA, S.CONFIRMADA}) == SITUACOES_QUE_OCUPAM_HORARIO


@pytest.mark.parametrize(
    ("situacao", "ocupa"),
    [
        (S.SOLICITADA, True),
        (S.CONFIRMADA, True),
        (S.RECUSADA, False),
        (S.CANCELADA, False),
        (S.CONCLUIDA, False),
    ],
)
def test_ocupa_horario_segue_o_conjunto(situacao, ocupa):
    # Assert
    assert situacao.ocupa_horario is ocupa


@pytest.mark.parametrize("situacao", [s for s in SituacaoReserva if s.eh_final])
def test_nenhum_estado_final_ocupa_horario(situacao):
    # Assert
    assert situacao.ocupa_horario is False
