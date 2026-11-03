from datetime import timedelta

import pytest

from reservas.application.casos_de_uso import (
    AlterarSituacaoReserva,
    ConsultarHistoricoDaReserva,
)
from reservas.domain.excecoes import ReservaNaoEncontrada
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import (
    AGORA,
    ANA,
    ATOR_ANA,
    GESTOR,
    ID_INEXISTENTE,
    OUTRA_PESSOA,
    RepositorioReservasEmMemoria,
    reserva_solicitada,
)
from reservas.tests.historico import verificar_historico_coerente

S = SituacaoReserva
DEPOIS = AGORA + timedelta(hours=3)


@pytest.fixture
def repositorio():
    return RepositorioReservasEmMemoria()


@pytest.fixture
def reserva_confirmada(repositorio):
    reserva = repositorio.salvar(reserva_solicitada())
    AlterarSituacaoReserva(repositorio, lambda: DEPOIS).executar(
        reserva_id=reserva.id, nova_situacao=S.CONFIRMADA, ator=GESTOR
    )
    return reserva


@pytest.mark.parametrize("ator", [GESTOR, ATOR_ANA], ids=["gestor", "dona"])
def test_quem_ve_a_reserva_recebe_o_historico_em_ordem(
    repositorio, reserva_confirmada, ator
):
    # Act
    historico = ConsultarHistoricoDaReserva(repositorio).executar(
        reserva_confirmada.id, ator=ator
    )

    # Assert
    verificar_historico_coerente(historico, S.CONFIRMADA)
    assert [r.autor_nome for r in historico] == [ANA.nome, GESTOR.nome]


def test_alterar_situacao_registra_o_momento_do_relogio_injetado(
    repositorio, reserva_confirmada
):
    # Act
    historico = repositorio.listar_historico(reserva_confirmada.id)

    # Assert
    assert [r.registrado_em for r in historico] == [AGORA, DEPOIS]


def test_historico_de_reserva_de_outra_pessoa_e_nao_encontrado(
    repositorio, reserva_confirmada
):
    # Act / Assert
    with pytest.raises(ReservaNaoEncontrada) as erro:
        ConsultarHistoricoDaReserva(repositorio).executar(
            reserva_confirmada.id, ator=OUTRA_PESSOA
        )

    assert erro.value.reserva_id == reserva_confirmada.id


def test_historico_de_reserva_inexistente_e_nao_encontrado(repositorio):
    # Act / Assert
    with pytest.raises(ReservaNaoEncontrada):
        ConsultarHistoricoDaReserva(repositorio).executar(ID_INEXISTENTE, ator=GESTOR)
