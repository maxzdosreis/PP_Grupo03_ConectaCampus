import logging
from datetime import date
from unittest.mock import MagicMock

import pytest

from reservas.application.ocupacao_do_dia import HorarioOcupado
from reservas.application.repositorio import (
    FiltrosDeReservas,
    Paginacao,
    RepositorioReservas,
)
from reservas.domain.excecoes import ConflitoDeHorario, ReservaDesatualizada
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.repositorio_com_agenda import (
    RepositorioReservasComAgenda,
)
from reservas.tests.fakes import (
    AGORA,
    DIA,
    GESTOR,
    AgendaDoDiaEmMemoria,
    RepositorioReservasEmMemoria,
    intervalo,
    momento_para,
    motivo_para,
    reserva_reconstituida,
    reserva_solicitada,
)

ESPACO = 3


class Cenario:
    def __init__(self, *, projecao_do_dia: bool = True, indisponivel: bool = False):
        self.repositorio = RepositorioReservasEmMemoria()
        self.agenda = AgendaDoDiaEmMemoria()
        self.acoes: list = []
        self.decorator = RepositorioReservasComAgenda(
            self.repositorio, self.agenda, self.acoes.append
        )
        if projecao_do_dia:
            self.agenda.substituir(
                ESPACO, DIA, {}, versao=self.agenda.versao(ESPACO, DIA)
            )
        self.agenda.indisponivel = indisponivel

    def executar_acoes(self, ordem=lambda acoes: acoes):
        for acao in ordem(list(self.acoes)):
            acao()
        self.acoes.clear()

    def salvar_nova(self, **sobrescritas):
        return self.decorator.salvar(reserva_solicitada(**sobrescritas))

    def mudar(self, reserva_id: int, nova: SituacaoReserva):
        reserva = self.decorator.obter_por_id(reserva_id)
        reserva.alterar_situacao(
            nova, motivo=motivo_para(nova), ator=GESTOR, agora=momento_para(nova)
        )
        return self.decorator.salvar(reserva)

    def agenda_do_dia(self):
        return self.agenda.listar(ESPACO, DIA)


def _situacoes(agenda) -> list[SituacaoReserva]:
    return [ocupado.situacao for ocupado in agenda or ()]


def test_reserva_criada_aparece_na_agenda_do_dia_com_projecao():
    # Arrange
    cenario = Cenario()

    # Act
    salva = cenario.salvar_nova()
    cenario.executar_acoes()

    # Assert
    assert cenario.agenda_do_dia() == (
        HorarioOcupado(intervalo=intervalo(), situacao=SituacaoReserva.SOLICITADA),
    )
    assert salva.id is not None


def test_reserva_criada_sem_projecao_nao_grava_nada_mas_avanca_a_versao():
    # Arrange
    cenario = Cenario(projecao_do_dia=False)

    # Act
    cenario.salvar_nova()
    cenario.executar_acoes()

    # Assert
    assert cenario.agenda_do_dia() is None
    assert cenario.agenda.versao(ESPACO, DIA) == 1


def test_a_acao_so_roda_quando_o_commit_a_executa():
    # Arrange
    cenario = Cenario()

    # Act
    cenario.salvar_nova()

    # Assert
    assert len(cenario.acoes) == 1
    assert cenario.agenda_do_dia() == ()


def test_confirmar_troca_a_situacao_do_membro():
    # Arrange
    cenario = Cenario()
    reserva_id = cenario.salvar_nova().id
    cenario.executar_acoes()

    # Act
    cenario.mudar(reserva_id, SituacaoReserva.CONFIRMADA)
    cenario.executar_acoes()

    # Assert
    assert _situacoes(cenario.agenda_do_dia()) == [SituacaoReserva.CONFIRMADA]


@pytest.mark.parametrize(
    "caminho",
    [
        [SituacaoReserva.CANCELADA],
        [SituacaoReserva.RECUSADA],
        [SituacaoReserva.CONFIRMADA, SituacaoReserva.CONCLUIDA],
        [SituacaoReserva.CONFIRMADA, SituacaoReserva.CANCELADA],
    ],
)
def test_situacao_que_libera_o_horario_remove_a_reserva_da_agenda(caminho):
    # Arrange
    cenario = Cenario()
    reserva_id = cenario.salvar_nova().id
    cenario.executar_acoes()

    # Act
    for situacao in caminho:
        cenario.mudar(reserva_id, situacao)
        cenario.executar_acoes()

    # Assert
    assert cenario.agenda_do_dia() == ()


def test_situacao_que_nao_ocupa_horario_nunca_chega_a_registrar(monkeypatch):
    # Arrange
    cenario = Cenario()
    reserva_id = cenario.salvar_nova().id
    cenario.executar_acoes()
    registrar = MagicMock()
    monkeypatch.setattr(cenario.agenda, "registrar", registrar)

    # Act
    cenario.mudar(reserva_id, SituacaoReserva.CANCELADA)
    cenario.executar_acoes()

    # Assert
    registrar.assert_not_called()


def test_salvar_que_lanca_conflito_nao_agenda_nada():
    # Arrange
    cenario = Cenario()
    cenario.salvar_nova()
    cenario.executar_acoes()

    # Act / Assert
    with pytest.raises(ConflitoDeHorario):
        cenario.salvar_nova()
    assert cenario.acoes == []


def test_salvar_de_reserva_desatualizada_nao_agenda_nada():
    # Arrange
    cenario = Cenario()
    reserva_id = cenario.salvar_nova().id
    cenario.executar_acoes()
    velha = cenario.decorator.obter_por_id(reserva_id)
    cenario.mudar(reserva_id, SituacaoReserva.CONFIRMADA)
    cenario.executar_acoes()
    velha.alterar_situacao(
        SituacaoReserva.CANCELADA,
        motivo=motivo_para(SituacaoReserva.CANCELADA),
        ator=GESTOR,
        agora=AGORA,
    )

    # Act / Assert
    with pytest.raises(ReservaDesatualizada):
        cenario.decorator.salvar(velha)
    assert cenario.acoes == []


def test_agenda_indisponivel_nao_lanca_e_deixa_um_aviso_com_o_id(caplog):
    # Arrange
    cenario = Cenario(indisponivel=True)
    salva = cenario.salvar_nova()

    # Act
    with caplog.at_level(logging.WARNING):
        cenario.executar_acoes()

    # Assert
    avisos = [r for r in caplog.records if r.levelno == logging.WARNING]
    assert len(avisos) == 1
    assert str(salva.id) in avisos[0].getMessage()
    assert "reconstrução" in avisos[0].getMessage()


def test_acoes_executadas_em_ordem_invertida_terminam_no_estado_atual():
    # Arrange
    cenario = Cenario()
    reserva_id = cenario.salvar_nova().id
    cenario.mudar(reserva_id, SituacaoReserva.CONFIRMADA)

    # Act: a ação da confirmação roda antes da ação da criação
    cenario.executar_acoes(ordem=lambda acoes: list(reversed(acoes)))

    # Assert
    assert _situacoes(cenario.agenda_do_dia()) == [SituacaoReserva.CONFIRMADA]


def test_acoes_em_ordem_invertida_de_uma_reserva_cancelada_deixam_a_agenda_vazia():
    # Arrange
    cenario = Cenario()
    reserva_id = cenario.salvar_nova().id
    cenario.mudar(reserva_id, SituacaoReserva.CANCELADA)

    # Act
    cenario.executar_acoes(ordem=lambda acoes: list(reversed(acoes)))

    # Assert
    assert cenario.agenda_do_dia() == ()


def test_reserva_que_sumiu_antes_da_acao_nao_toca_na_agenda():
    # Arrange
    interno = MagicMock(spec=RepositorioReservas)
    interno.salvar.return_value = reserva_reconstituida()
    interno.obter_por_id.return_value = None
    agenda = MagicMock()
    acoes: list = []
    decorator = RepositorioReservasComAgenda(interno, agenda, acoes.append)

    # Act
    decorator.salvar(reserva_solicitada())
    acoes[0]()

    # Assert
    assert agenda.mock_calls == []


def test_entidade_sem_id_nao_toca_na_agenda():
    # Arrange
    interno = MagicMock(spec=RepositorioReservas)
    interno.salvar.return_value = reserva_solicitada()
    agenda = MagicMock()
    acoes: list = []
    decorator = RepositorioReservasComAgenda(interno, agenda, acoes.append)

    # Act
    decorator.salvar(reserva_solicitada())
    acoes[0]()

    # Assert
    interno.obter_por_id.assert_not_called()
    assert agenda.mock_calls == []


def test_tentativa_recusada_e_leituras_nao_tocam_na_agenda_e_sao_delegadas():
    # Arrange
    interno = MagicMock(spec=RepositorioReservas)
    agenda = MagicMock()
    acoes: list = []
    decorator = RepositorioReservasComAgenda(interno, agenda, acoes.append)
    filtros, paginacao, registro = FiltrosDeReservas(), Paginacao(), object()

    # Act
    decorator.em_transacao()
    decorator.gravar_tentativa_recusada(12, registro)
    decorator.obter_por_id(12)
    decorator.listar(filtros, paginacao)
    decorator.listar_que_ocupam_horario(ESPACO, DIA)
    decorator.listar_ativas_a_partir_de(ESPACO, AGORA)
    decorator.listar_historico(12)

    # Assert
    interno.em_transacao.assert_called_once_with()
    interno.gravar_tentativa_recusada.assert_called_once_with(12, registro)
    interno.obter_por_id.assert_called_once_with(12)
    interno.listar.assert_called_once_with(filtros, paginacao)
    interno.listar_que_ocupam_horario.assert_called_once_with(ESPACO, DIA)
    interno.listar_ativas_a_partir_de.assert_called_once_with(ESPACO, AGORA)
    interno.listar_historico.assert_called_once_with(12)
    assert agenda.mock_calls == []
    assert acoes == []


def test_o_padrao_de_agendamento_usa_o_on_commit_robusto(monkeypatch):
    # Arrange
    chamadas = []
    monkeypatch.setattr(
        "reservas.infrastructure.repositorio_com_agenda.transaction.on_commit",
        lambda acao, **opcoes: chamadas.append((acao, opcoes)),
    )
    decorator = RepositorioReservasComAgenda(
        RepositorioReservasEmMemoria(), AgendaDoDiaEmMemoria()
    )

    # Act
    decorator.salvar(reserva_solicitada())

    # Assert
    assert len(chamadas) == 1
    assert chamadas[0][1] == {"robust": True}


def test_data_da_agenda_e_a_do_intervalo_da_reserva():
    # Arrange
    outro_dia = date(2026, 10, 26)
    cenario = Cenario()
    cenario.agenda.substituir(
        ESPACO, outro_dia, {}, versao=cenario.agenda.versao(ESPACO, outro_dia)
    )

    # Act
    cenario.salvar_nova(data=outro_dia)
    cenario.executar_acoes()

    # Assert
    assert cenario.agenda_do_dia() == ()
    assert len(cenario.agenda.listar(ESPACO, outro_dia)) == 1
