import pytest

from compartilhado.domain.erros import CampoObrigatorioAusente
from espacos.application.casos_de_uso import (
    AtivarEspaco,
    CadastrarEspaco,
    DesativarEspaco,
    EditarEspaco,
    ListarEspacos,
    ObterEspaco,
    VerificarEspacoDisponivel,
)
from espacos.domain.excecoes import (
    CapacidadeInvalida,
    EspacoInativo,
    EspacoNaoEncontrado,
    NomeDeEspacoJaCadastrado,
    TipoDeEspacoInvalido,
)
from espacos.domain.tipo_espaco import TipoEspaco
from espacos.tests.fakes import (
    ID_INEXISTENTE,
    RepositorioEspacosEmMemoria,
    dados_validos,
    nomes,
    novo_espaco,
)


@pytest.fixture
def repositorio():
    return RepositorioEspacosEmMemoria()


def _salvar(repositorio, nome, tipo, *, ativo=True):
    return repositorio.salvar(novo_espaco(nome=nome, tipo=tipo, ativo=ativo))


def test_cadastrar_espaco_valido_devolve_com_id_e_aparece_na_listagem(repositorio):
    # Act
    espaco = CadastrarEspaco(repositorio).executar(**dados_validos())

    # Assert
    assert espaco.id is not None
    assert espaco.tipo is TipoEspaco.GINASIO
    assert ListarEspacos(repositorio).executar() == [espaco]


def test_cadastrar_nome_repetido_com_caixa_e_espacos_diferentes_lanca_conflito(
    repositorio,
):
    # Arrange
    cadastrar = CadastrarEspaco(repositorio)
    cadastrar.executar(**dados_validos(nome="Ginásio A"))

    # Act
    with pytest.raises(NomeDeEspacoJaCadastrado):
        cadastrar.executar(**dados_validos(nome="  ginásio a "))

    # Assert
    assert nomes(repositorio.listar()) == ["Ginásio A"]


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
        CadastrarEspaco(repositorio).executar(**dados_validos(**sobrescritas))

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
    assert nomes(espacos) == nomes_esperados


def test_obter_espaco_existente_devolve_o_espaco(repositorio):
    # Arrange
    cadastrado = CadastrarEspaco(repositorio).executar(**dados_validos())

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


def test_verificar_espaco_disponivel_ativo_devolve_o_espaco(repositorio):
    # Arrange
    salvo = _salvar(repositorio, "Ginásio Novo", TipoEspaco.GINASIO)

    # Act
    espaco = VerificarEspacoDisponivel(repositorio).executar(salvo.id)

    # Assert
    assert espaco == salvo
    assert espaco.nome == "Ginásio Novo"


def test_verificar_espaco_disponivel_inativo_lanca_espaco_inativo(repositorio):
    # Arrange
    salvo = _salvar(repositorio, "Ginásio Antigo", TipoEspaco.GINASIO, ativo=False)

    # Act / Assert
    with pytest.raises(EspacoInativo):
        VerificarEspacoDisponivel(repositorio).executar(salvo.id)


@pytest.mark.parametrize("nome", ["Ginásio A", "  GINÁSIO   a "])
def test_editar_mantendo_o_proprio_nome_nao_acusa_duplicidade(repositorio, nome):
    # Arrange
    cadastrado = CadastrarEspaco(repositorio).executar(**dados_validos())

    # Act
    editado = EditarEspaco(repositorio).executar(
        cadastrado.id, nome=nome, capacidade=80
    )

    # Assert
    assert editado.capacidade == 80
    assert repositorio.obter_por_id(cadastrado.id).capacidade == 80


def test_editar_o_tipo_grava_o_tipo_novo_e_mantem_o_resto(repositorio):
    # Arrange
    cadastrado = CadastrarEspaco(repositorio).executar(**dados_validos())

    # Act
    editado = EditarEspaco(repositorio).executar(cadastrado.id, tipo="QUADRA_DE_AREIA")

    # Assert
    guardado = repositorio.obter_por_id(cadastrado.id)
    assert editado.tipo is TipoEspaco.QUADRA_DE_AREIA
    assert (guardado.nome, guardado.tipo, guardado.capacidade) == (
        "Ginásio A",
        TipoEspaco.QUADRA_DE_AREIA,
        50,
    )


def test_editar_para_o_nome_de_outro_espaco_lanca_conflito_sem_gravar(repositorio):
    # Arrange
    cadastrar = CadastrarEspaco(repositorio)
    cadastrar.executar(**dados_validos(nome="Ginásio A"))
    outro = cadastrar.executar(**dados_validos(nome="Ginásio B"))
    gravacoes_antes = repositorio.chamadas_de_salvar

    # Act
    with pytest.raises(NomeDeEspacoJaCadastrado):
        EditarEspaco(repositorio).executar(outro.id, nome="ginásio a", capacidade=5)

    # Assert
    guardado = repositorio.obter_por_id(outro.id)
    assert (guardado.nome, guardado.capacidade) == ("Ginásio B", 50)
    assert repositorio.chamadas_de_salvar == gravacoes_antes


def test_editar_com_dado_invalido_nao_grava(repositorio):
    # Arrange
    cadastrado = CadastrarEspaco(repositorio).executar(**dados_validos())

    # Act
    with pytest.raises(CapacidadeInvalida):
        EditarEspaco(repositorio).executar(
            cadastrado.id, nome="Ginásio Novo", capacidade=0
        )

    # Assert
    assert nomes(repositorio.listar()) == ["Ginásio A"]


def test_desativar_grava_o_espaco_inativo(repositorio):
    # Arrange
    cadastrado = CadastrarEspaco(repositorio).executar(**dados_validos())

    # Act
    desativado = DesativarEspaco(repositorio).executar(cadastrado.id)

    # Assert
    assert desativado.ativo is False
    assert repositorio.obter_por_id(cadastrado.id).ativo is False


def test_ativar_grava_o_espaco_ativo(repositorio):
    # Arrange
    cadastrado = CadastrarEspaco(repositorio).executar(**dados_validos())
    DesativarEspaco(repositorio).executar(cadastrado.id)

    # Act
    reativado = AtivarEspaco(repositorio).executar(cadastrado.id)

    # Assert
    assert reativado.ativo is True
    assert repositorio.obter_por_id(cadastrado.id).ativo is True


@pytest.mark.parametrize(
    "executar",
    [
        lambda repositorio: EditarEspaco(repositorio).executar(
            ID_INEXISTENTE, capacidade=10
        ),
        lambda repositorio: DesativarEspaco(repositorio).executar(ID_INEXISTENTE),
        lambda repositorio: AtivarEspaco(repositorio).executar(ID_INEXISTENTE),
    ],
    ids=["editar", "desativar", "ativar"],
)
def test_acoes_em_espaco_inexistente_lancam_espaco_nao_encontrado(
    repositorio, executar
):
    # Act
    with pytest.raises(EspacoNaoEncontrado) as erro:
        executar(repositorio)

    # Assert
    assert erro.value.espaco_id == ID_INEXISTENTE


def test_verificar_espaco_disponivel_inexistente_lanca_espaco_nao_encontrado(
    repositorio,
):
    # Act
    with pytest.raises(EspacoNaoEncontrado) as erro:
        VerificarEspacoDisponivel(repositorio).executar(ID_INEXISTENTE)

    # Assert
    assert erro.value.espaco_id == ID_INEXISTENTE
