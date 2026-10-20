import pytest

from compartilhado.domain.erros import CampoObrigatorioAusente
from espacos.application.casos_de_uso import CadastrarEspaco, ListarEspacos, ObterEspaco
from espacos.domain.espaco_esportivo import EspacoEsportivo
from espacos.domain.excecoes import (
    CapacidadeInvalida,
    EspacoNaoEncontrado,
    NomeDeEspacoJaCadastrado,
    TipoDeEspacoInvalido,
)
from espacos.domain.tipo_espaco import TipoEspaco
from espacos.tests.fakes import RepositorioEspacosEmMemoria

ID_INEXISTENTE = 9999


@pytest.fixture
def repositorio():
    return RepositorioEspacosEmMemoria()


def _dados_validos(**sobrescritas):
    dados = {"nome": "Ginásio A", "tipo": "GINASIO", "capacidade": 50}
    dados.update(sobrescritas)
    return dados


def _salvar(repositorio, nome, tipo, *, ativo=True):
    repositorio.salvar(
        EspacoEsportivo(nome=nome, tipo=tipo, capacidade=10, ativo=ativo)
    )


def _nomes(espacos):
    return [espaco.nome for espaco in espacos]


def test_cadastrar_espaco_valido_devolve_com_id_e_aparece_na_listagem(repositorio):
    # Act
    espaco = CadastrarEspaco(repositorio).executar(**_dados_validos())

    # Assert
    assert espaco.id is not None
    assert espaco.tipo is TipoEspaco.GINASIO
    assert ListarEspacos(repositorio).executar() == [espaco]


def test_cadastrar_nome_repetido_com_caixa_e_espacos_diferentes_lanca_conflito(
    repositorio,
):
    # Arrange
    cadastrar = CadastrarEspaco(repositorio)
    cadastrar.executar(**_dados_validos(nome="Ginásio A"))

    # Act
    with pytest.raises(NomeDeEspacoJaCadastrado):
        cadastrar.executar(**_dados_validos(nome="  ginásio a "))

    # Assert
    assert _nomes(repositorio.listar()) == ["Ginásio A"]


@pytest.mark.parametrize(
    ("sobrescritas", "excecao"),
    [
        ({"nome": "   "}, CampoObrigatorioAusente),
        ({"capacidade": 0}, CapacidadeInvalida),
        ({"tipo": "PISCINA"}, TipoDeEspacoInvalido),
    ],
    ids=["nome-vazio", "capacidade-zero", "tipo-desconhecido"],
)
def test_cadastrar_com_dado_invalido_propaga_erro_do_dominio_sem_salvar(
    repositorio, sobrescritas, excecao
):
    # Act
    with pytest.raises(excecao):
        CadastrarEspaco(repositorio).executar(**_dados_validos(**sobrescritas))

    # Assert
    assert repositorio.listar() == []


@pytest.mark.parametrize(
    ("filtros", "nomes_esperados"),
    [
        ({}, ["Campo Norte", "Ginásio Antigo", "Ginásio Novo"]),
        ({"apenas_ativos": True}, ["Campo Norte", "Ginásio Novo"]),
        ({"tipo": TipoEspaco.GINASIO}, ["Ginásio Antigo", "Ginásio Novo"]),
        ({"apenas_ativos": True, "tipo": TipoEspaco.GINASIO}, ["Ginásio Novo"]),
    ],
    ids=["sem-filtro", "apenas-ativos", "por-tipo", "ativos-e-tipo"],
)
def test_listar_repassa_os_filtros_ao_repositorio(
    repositorio, filtros, nomes_esperados
):
    # Arrange
    _salvar(repositorio, "Ginásio Antigo", TipoEspaco.GINASIO, ativo=False)
    _salvar(repositorio, "Campo Norte", TipoEspaco.CAMPO_DE_FUTEBOL)
    _salvar(repositorio, "Ginásio Novo", TipoEspaco.GINASIO)

    # Act
    espacos = ListarEspacos(repositorio).executar(**filtros)

    # Assert
    assert _nomes(espacos) == nomes_esperados


def test_obter_espaco_existente_devolve_o_espaco(repositorio):
    # Arrange
    cadastrado = CadastrarEspaco(repositorio).executar(**_dados_validos())

    # Act
    obtido = ObterEspaco(repositorio).executar(cadastrado.id)

    # Assert
    assert obtido == cadastrado
    assert obtido.nome == "Ginásio A"


def test_obter_espaco_inexistente_lanca_espaco_nao_encontrado(repositorio):
    # Act
    with pytest.raises(EspacoNaoEncontrado) as erro:
        ObterEspaco(repositorio).executar(ID_INEXISTENTE)

    # Assert
    assert erro.value.espaco_id == ID_INEXISTENTE
