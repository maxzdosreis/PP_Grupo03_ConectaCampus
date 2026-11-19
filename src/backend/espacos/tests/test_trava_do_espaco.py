from datetime import time

import pytest

from espacos.application.casos_de_uso import (
    EditarEspaco,
    VerificarEspacoParaReservar,
)
from espacos.domain.excecoes import (
    EspacoInativo,
    EspacoNaoEncontrado,
    HorarioIncompativelComReservas,
)
from espacos.tests.fakes import (
    ID_INEXISTENTE,
    RepositorioEspacosEmMemoria,
    ReservasDoEspacoFake,
    novo_espaco,
)


@pytest.fixture
def eventos():
    return []


@pytest.fixture
def repositorio(eventos):
    return RepositorioEspacosEmMemoria(eventos)


def _cadastrar(repositorio, eventos, **sobrescritas):
    espaco = repositorio.salvar(novo_espaco(**sobrescritas))
    eventos.clear()
    return espaco


def test_editar_o_horario_trava_o_espaco_antes_de_contar_e_grava_na_mesma_transacao(
    repositorio, eventos
):
    # Arrange
    espaco = _cadastrar(repositorio, eventos)
    reservas = ReservasDoEspacoFake(eventos=eventos)

    # Act
    EditarEspaco(repositorio, reservas).executar(espaco.id, fechamento=time(20, 0))

    # Assert
    assert eventos == ["abrir", "travar", "contar", "salvar", "fechar"]
    assert repositorio.ids_travados == [espaco.id]


def test_editar_o_horario_recusado_por_reservas_nao_grava_e_fecha_a_transacao(
    repositorio, eventos
):
    # Arrange
    espaco = _cadastrar(repositorio, eventos)
    reservas = ReservasDoEspacoFake(fora_da_janela=1, eventos=eventos)

    # Act
    with pytest.raises(HorarioIncompativelComReservas):
        EditarEspaco(repositorio, reservas).executar(espaco.id, fechamento=time(20, 0))

    # Assert
    assert eventos == ["abrir", "travar", "contar", "fechar"]
    assert repositorio.transacoes_abertas == 0


def test_editar_sem_mudar_o_horario_nao_trava_o_espaco(repositorio, eventos):
    # Arrange
    espaco = _cadastrar(repositorio, eventos)
    reservas = ReservasDoEspacoFake(eventos=eventos)

    # Act
    EditarEspaco(repositorio, reservas).executar(espaco.id, capacidade=50)

    # Assert
    assert eventos == ["abrir", "salvar", "fechar"]
    assert repositorio.ids_travados == []


def test_editar_espaco_inexistente_fecha_a_transacao_sem_travar(repositorio, eventos):
    # Act
    with pytest.raises(EspacoNaoEncontrado):
        EditarEspaco(repositorio, ReservasDoEspacoFake(eventos=eventos)).executar(
            ID_INEXISTENTE, capacidade=50
        )

    # Assert
    assert eventos == ["abrir", "fechar"]


def test_verificar_para_reservar_trava_o_espaco_antes_de_lê_lo(repositorio, eventos):
    # Arrange
    espaco = _cadastrar(repositorio, eventos)

    # Act
    with repositorio.em_transacao():
        encontrado = VerificarEspacoParaReservar(repositorio).executar(espaco.id)

    # Assert
    assert encontrado.id == espaco.id
    assert repositorio.ids_travados == [espaco.id]


def test_verificar_para_reservar_espaco_inexistente_lanca_nao_encontrado(
    repositorio, eventos
):
    # Arrange

    # Act / Assert
    with pytest.raises(EspacoNaoEncontrado), repositorio.em_transacao():
        VerificarEspacoParaReservar(repositorio).executar(ID_INEXISTENTE)


def test_verificar_para_reservar_espaco_inativo_lanca_espaco_inativo(
    repositorio, eventos
):
    # Arrange
    espaco = _cadastrar(repositorio, eventos, ativo=False)

    # Act / Assert
    with pytest.raises(EspacoInativo), repositorio.em_transacao():
        VerificarEspacoParaReservar(repositorio).executar(espaco.id)


def test_o_fake_recusa_travar_fora_de_uma_transacao(repositorio):
    # Act / Assert
    with pytest.raises(AssertionError, match="fora de uma transação"):
        repositorio.travar(1)
