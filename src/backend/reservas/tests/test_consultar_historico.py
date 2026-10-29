from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest

from reservas.application.casos_de_uso import (
    AlterarSituacaoReserva,
    ConsultarHistoricoDaReserva,
)
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.excecoes import ReservaNaoEncontrada
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva
from reservas.domain.solicitante import Solicitante
from reservas.tests.fakes import RepositorioReservasEmMemoria
from reservas.tests.historico import verificar_historico_coerente

S = SituacaoReserva
SAO_PAULO = ZoneInfo("America/Sao_Paulo")
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=SAO_PAULO)
DEPOIS = AGORA + timedelta(hours=3)
ANA = Solicitante(usuario_id=7, nome="Ana Souza", matricula="2026001")
GESTOR = Ator(usuario_id=1, nome="Gestora de Teste", papel=PapelDoAtor.GESTOR)
DONA = Ator(usuario_id=ANA.usuario_id, nome=ANA.nome, papel=PapelDoAtor.SOLICITANTE)
OUTRA_PESSOA = Ator(usuario_id=99, nome="Outra Pessoa", papel=PapelDoAtor.SOLICITANTE)
ID_INEXISTENTE = 9999


@pytest.fixture
def repositorio():
    return RepositorioReservasEmMemoria()


@pytest.fixture
def reserva_confirmada(repositorio):
    reserva = repositorio.salvar(
        Reserva.solicitar(
            espaco_id=1,
            solicitante=ANA,
            data=date(2026, 10, 25),
            hora_inicio=time(10, 0),
            hora_fim=time(11, 0),
            finalidade="Treino",
            agora=AGORA,
        )
    )
    AlterarSituacaoReserva(repositorio, lambda: DEPOIS).executar(
        reserva_id=reserva.id, nova_situacao=S.CONFIRMADA, ator=GESTOR
    )
    return reserva


@pytest.mark.parametrize("ator", [GESTOR, DONA], ids=["gestor", "dona"])
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
