import logging

import pytest

from espacos.domain.excecoes import EspacoNaoEncontrado
from espacos.infrastructure.repositorio_que_invalida import (
    RepositorioEspacosQueInvalida,
)
from espacos.tests.fakes import (
    CacheDeEspacosEmMemoria,
    RepositorioEspacosEmMemoria,
    novo_espaco,
)


class _Commit:
    def __init__(self) -> None:
        self.pendentes = []

    def __call__(self, acao):
        self.pendentes.append(acao)

    def efetivar(self) -> None:
        for acao in self.pendentes:
            acao()

    def descartar(self) -> None:
        self.pendentes.clear()


@pytest.fixture
def interno():
    return RepositorioEspacosEmMemoria()


@pytest.fixture
def cache():
    return CacheDeEspacosEmMemoria()


@pytest.fixture
def commit():
    return _Commit()


@pytest.fixture
def repositorio(interno, cache, commit):
    return RepositorioEspacosQueInvalida(interno, cache, apos_o_commit=commit)


def test_salvar_so_invalida_depois_do_commit(repositorio, cache, commit):
    # Act
    salvo = repositorio.salvar(novo_espaco())

    # Assert
    assert cache.invalidacoes == []
    commit.efetivar()
    assert cache.invalidacoes == [salvo.id]


@pytest.mark.parametrize("operacao", ["editar", "desativar", "reativar"])
def test_invalida_depois_de_cada_tipo_de_escrita(repositorio, cache, commit, operacao):
    # Arrange
    espaco = repositorio.salvar(novo_espaco())
    commit.descartar()
    if operacao == "reativar":
        espaco.desativar()
        repositorio.salvar(espaco)
        commit.descartar()
        espaco = repositorio.obter_por_id(espaco.id)

    # Act
    if operacao == "editar":
        espaco.alterar_dados(nome="Outro nome")
    elif operacao == "desativar":
        espaco.desativar()
    else:
        espaco.ativar()
    repositorio.salvar(espaco)
    commit.efetivar()

    # Assert
    assert cache.invalidacoes == [espaco.id]


def test_rollback_nao_invalida(repositorio, cache, commit):
    # Arrange
    repositorio.salvar(novo_espaco())

    # Act
    commit.descartar()
    commit.efetivar()

    # Assert
    assert cache.invalidacoes == []


def test_salvar_que_falha_nao_agenda_invalidacao(repositorio, cache, commit):
    # Act
    with pytest.raises(EspacoNaoEncontrado):
        repositorio.salvar(novo_espaco(id=99))

    # Assert
    commit.efetivar()
    assert cache.invalidacoes == []


def test_falha_do_cache_na_invalidacao_so_vira_log(repositorio, cache, commit, caplog):
    # Arrange
    salvo = repositorio.salvar(novo_espaco())
    cache.indisponivel = True

    # Act
    with caplog.at_level(logging.WARNING):
        commit.efetivar()

    # Assert
    assert "não invalidado" in caplog.text
    assert repositorio.obter_por_id(salvo.id) == salvo


def test_delega_os_demais_metodos_do_protocolo(repositorio, interno):
    # Arrange
    espaco = repositorio.salvar(novo_espaco(nome="Ginásio A"))

    # Act e Assert
    assert repositorio.obter_por_id(espaco.id) == espaco
    assert repositorio.listar() == [espaco]
    assert repositorio.listar(apenas_ativos=True, tipo=espaco.tipo) == [espaco]
    assert repositorio.existe_com_nome("ginásio a") is True
    assert repositorio.existe_com_nome("ginásio a", ignorar_id=espaco.id) is False
    with repositorio.em_transacao():
        repositorio.travar(espaco.id)
    assert interno.ids_travados == [espaco.id]
