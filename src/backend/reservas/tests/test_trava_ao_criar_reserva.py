from datetime import time

import pytest

from reservas.application.casos_de_uso import CriarReserva
from reservas.domain.excecoes import DataRetroativa, ForaDoHorarioDeFuncionamento
from reservas.tests.fakes import (
    AGORA,
    ANA,
    DIA,
    ConsultaDeEspacosEmMemoria,
    RepositorioReservasEmMemoria,
    espaco_reservavel,
)

QUADRA = espaco_reservavel(1, "Quadra Coberta")


def _pedido(consulta, repositorio, **sobrescritas):
    dados = {
        "espaco_id": QUADRA.id,
        "solicitante": ANA,
        "data": DIA,
        "hora_inicio": time(10, 0),
        "hora_fim": time(11, 0),
        "finalidade": "Treino",
    }
    dados.update(sobrescritas)
    return CriarReserva(repositorio, consulta, lambda: AGORA).executar(**dados)


def test_criar_trava_o_espaco_antes_de_validar_o_horario_e_grava_na_mesma_transacao():
    # Arrange
    eventos = []
    consulta = ConsultaDeEspacosEmMemoria([QUADRA], eventos=eventos)
    repositorio = RepositorioReservasEmMemoria(eventos)

    # Act
    _pedido(consulta, repositorio)

    # Assert
    assert eventos == ["abrir", "travar", "listar", "salvar", "fechar"]


def test_pedido_fora_do_horario_do_espaco_travado_e_recusado_sem_gravar():
    # Arrange
    eventos = []
    consulta = ConsultaDeEspacosEmMemoria([QUADRA], eventos=eventos)
    repositorio = RepositorioReservasEmMemoria(eventos)

    # Act
    with pytest.raises(ForaDoHorarioDeFuncionamento):
        _pedido(consulta, repositorio, hora_inicio=time(5, 0), hora_fim=time(6, 0))

    # Assert
    assert eventos == ["abrir", "travar", "fechar"]
    assert repositorio.transacoes_abertas == 0


def test_data_retroativa_e_recusada_antes_de_abrir_a_transacao_e_de_travar():
    # Arrange
    eventos = []
    consulta = ConsultaDeEspacosEmMemoria([QUADRA], eventos=eventos)
    repositorio = RepositorioReservasEmMemoria(eventos)

    # Act
    with pytest.raises(DataRetroativa):
        _pedido(consulta, repositorio, data=AGORA.date().replace(year=2020))

    # Assert
    assert eventos == []
