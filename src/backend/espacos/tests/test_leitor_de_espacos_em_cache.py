import logging

import pytest

from espacos.application.casos_de_uso import (
    ObterEspaco,
    VerificarEspacoDisponivel,
    VerificarEspacoParaReservar,
)
from espacos.application.leitor_de_espacos_em_cache import LeitorDeEspacosComCache
from espacos.domain.excecoes import EspacoInativo, EspacoNaoEncontrado
from espacos.tests.fakes import (
    ID_INEXISTENTE,
    CacheDeEspacosEmMemoria,
    RepositorioEspacosEmMemoria,
    novo_espaco,
)


@pytest.fixture
def repositorio():
    return RepositorioEspacosEmMemoria()


@pytest.fixture
def cache():
    return CacheDeEspacosEmMemoria()


@pytest.fixture
def leitor(repositorio, cache):
    return LeitorDeEspacosComCache(repositorio, cache)


def test_hit_nao_toca_o_repositorio(leitor, repositorio, cache):
    # Arrange
    espaco = repositorio.salvar(novo_espaco())
    leitor.obter_por_id(espaco.id)
    repositorio.leituras = 0

    # Act
    lido = leitor.obter_por_id(espaco.id)

    # Assert
    assert lido == espaco
    assert lido.nome == espaco.nome
    assert repositorio.leituras == 0


def test_miss_le_o_repositorio_e_guarda(leitor, repositorio, cache):
    # Arrange
    espaco = repositorio.salvar(novo_espaco())

    # Act
    lido = leitor.obter_por_id(espaco.id)

    # Assert
    assert lido == espaco
    assert cache.guardado(espaco.id)
    assert repositorio.leituras == 1


def test_cache_indisponivel_le_o_repositorio_sem_lancar(
    leitor, repositorio, cache, caplog
):
    # Arrange
    espaco = repositorio.salvar(novo_espaco())
    cache.indisponivel = True

    # Act
    with caplog.at_level(logging.WARNING):
        lido = leitor.obter_por_id(espaco.id)

    # Assert
    assert lido == espaco
    assert "indisponível" in caplog.text


def test_falha_ao_guardar_ainda_devolve_o_espaco(leitor, repositorio, cache, caplog):
    # Arrange
    espaco = repositorio.salvar(novo_espaco())
    guardar = cache.guardar

    def guardar_que_falha(*args, **kwargs):
        cache.indisponivel = True
        return guardar(*args, **kwargs)

    cache.guardar = guardar_que_falha

    # Act
    with caplog.at_level(logging.WARNING):
        lido = leitor.obter_por_id(espaco.id)

    # Assert
    assert lido == espaco
    assert "não guardado" in caplog.text


def test_espaco_inexistente_nao_e_guardado_e_continua_nao_encontrado(leitor, cache):
    # Act e Assert
    with pytest.raises(EspacoNaoEncontrado):
        ObterEspaco(leitor).executar(ID_INEXISTENTE)
    assert not cache.guardado(ID_INEXISTENTE)


def test_espaco_inativo_vindo_do_cache_continua_lancando_espaco_inativo(
    leitor, repositorio, cache
):
    # Arrange
    espaco = repositorio.salvar(novo_espaco())
    espaco.desativar()
    repositorio.salvar(espaco)
    leitor.obter_por_id(espaco.id)
    repositorio.leituras = 0

    # Act e Assert
    with pytest.raises(EspacoInativo):
        VerificarEspacoDisponivel(leitor).executar(espaco.id)
    assert repositorio.leituras == 0


def test_versao_que_avanca_entre_a_leitura_e_a_gravacao_impede_de_guardar(
    repositorio, cache
):
    # Arrange
    espaco = repositorio.salvar(novo_espaco())

    class RepositorioQueInvalidaNoMeio(RepositorioEspacosEmMemoria):
        def obter_por_id(self, espaco_id):
            lido = repositorio.obter_por_id(espaco_id)
            cache.invalidar(espaco_id)
            return lido

    leitor = LeitorDeEspacosComCache(RepositorioQueInvalidaNoMeio(), cache)

    # Act
    lido = leitor.obter_por_id(espaco.id)

    # Assert
    assert lido == espaco
    assert not cache.guardado(espaco.id)


def test_entrada_quebrada_do_cache_vira_miss(leitor, repositorio, cache):
    # Arrange
    espaco = repositorio.salvar(novo_espaco())
    leitor.obter_por_id(espaco.id)
    cache.quebrados.add(espaco.id)
    repositorio.leituras = 0

    # Act
    lido = leitor.obter_por_id(espaco.id)

    # Assert
    assert lido == espaco
    assert repositorio.leituras == 1
    assert cache.guardado(espaco.id)


def test_a_trava_e_a_validacao_para_reservar_leem_o_repositorio_simples(
    repositorio, cache
):
    # Arrange
    espaco = repositorio.salvar(novo_espaco())
    envenenado = novo_espaco(id=espaco.id, ativo=False)
    cache.guardar(envenenado, versao=cache.versao(espaco.id))
    repositorio.leituras = 0

    # Act
    with repositorio.em_transacao():
        lido = VerificarEspacoParaReservar(repositorio).executar(espaco.id)

    # Assert
    assert lido.ativo is True
    assert repositorio.ids_travados == [espaco.id]
    assert repositorio.leituras == 1
