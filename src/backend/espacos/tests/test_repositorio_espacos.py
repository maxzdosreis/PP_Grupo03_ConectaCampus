import pytest
from django.db import IntegrityError, connection
from django.test.utils import CaptureQueriesContext

from espacos.domain.excecoes import (
    EspacoDesatualizado,
    EspacoNaoEncontrado,
    NomeDeEspacoJaCadastrado,
)
from espacos.domain.tipo_espaco import TipoEspaco
from espacos.infrastructure.models import EspacoEsportivoModel
from espacos.infrastructure.repositorio_django import RepositorioEspacosDjango
from espacos.tests.fakes import (
    ID_INEXISTENTE,
    RepositorioEspacosEmMemoria,
    nomes,
    novo_espaco,
)


@pytest.fixture(
    params=[
        pytest.param(
            RepositorioEspacosDjango, marks=pytest.mark.django_db, id="django"
        ),
        pytest.param(RepositorioEspacosEmMemoria, id="memoria"),
    ]
)
def repositorio(request):
    return request.param()


def _salvar_espacos_para_listagem(repositorio):
    repositorio.salvar(
        novo_espaco(nome="Quadra Coberta", tipo=TipoEspaco.QUADRA_POLIESPORTIVA)
    )
    repositorio.salvar(
        novo_espaco(nome="Ginasio Antigo", tipo=TipoEspaco.GINASIO, ativo=False)
    )
    repositorio.salvar(
        novo_espaco(nome="Campo Norte", tipo=TipoEspaco.CAMPO_DE_FUTEBOL)
    )
    repositorio.salvar(novo_espaco(nome="Ginasio Novo", tipo=TipoEspaco.GINASIO))


def test_salvar_espaco_novo_atribui_id_e_permite_obter_igual(repositorio):
    # Act
    salvo = repositorio.salvar(novo_espaco(tipo=TipoEspaco.GINASIO))

    # Assert
    obtido = repositorio.obter_por_id(salvo.id)
    assert salvo.id is not None
    assert obtido == salvo
    assert obtido.nome == "Quadra Central"
    assert obtido.tipo is TipoEspaco.GINASIO
    assert obtido.capacidade == 20
    assert obtido.ativo is True


def test_salvar_espaco_existente_atualiza_sem_criar_outro(repositorio):
    # Arrange
    salvo = repositorio.salvar(novo_espaco())
    alterado = repositorio.obter_por_id(salvo.id)
    alterado.alterar_dados(nome="Quadra Reformada", capacidade=30)
    alterado.desativar()

    # Act
    atualizado = repositorio.salvar(alterado)

    # Assert
    obtido = repositorio.obter_por_id(salvo.id)
    assert atualizado.id == salvo.id
    assert (obtido.nome, obtido.capacidade, obtido.ativo) == (
        "Quadra Reformada",
        30,
        False,
    )
    assert len(repositorio.listar()) == 1


def test_salvar_espaco_existente_mantendo_o_proprio_nome_nao_conflita(repositorio):
    # Arrange
    salvo = repositorio.salvar(novo_espaco())
    alterado = repositorio.obter_por_id(salvo.id)
    alterado.alterar_dados(nome="Quadra Central", capacidade=40)

    # Act
    atualizado = repositorio.salvar(alterado)

    # Assert
    assert atualizado.capacidade == 40
    assert repositorio.obter_por_id(salvo.id).capacidade == 40


def test_salvar_com_id_inexistente_lanca_espaco_nao_encontrado(repositorio):
    # Act
    with pytest.raises(EspacoNaoEncontrado) as erro:
        repositorio.salvar(novo_espaco(id=ID_INEXISTENTE))

    # Assert
    assert erro.value.espaco_id == ID_INEXISTENTE
    assert repositorio.listar() == []


def test_obter_por_id_inexistente_devolve_none(repositorio):
    # Act
    obtido = repositorio.obter_por_id(ID_INEXISTENTE)

    # Assert
    assert obtido is None


def test_salvar_nome_repetido_com_caixa_diferente_lanca_nome_ja_cadastrado(
    repositorio,
):
    # Arrange
    repositorio.salvar(novo_espaco(nome="Ginásio A"))

    # Act
    with pytest.raises(NomeDeEspacoJaCadastrado):
        repositorio.salvar(novo_espaco(nome="ginásio a"))

    # Assert
    assert nomes(repositorio.listar()) == ["Ginásio A"]


def test_renomear_para_o_nome_de_outro_espaco_lanca_nome_ja_cadastrado(repositorio):
    # Arrange
    repositorio.salvar(novo_espaco(nome="Ginásio A"))
    outro = repositorio.salvar(novo_espaco(nome="Ginásio B"))
    renomeado = repositorio.obter_por_id(outro.id)
    renomeado.alterar_dados(nome="GINÁSIO A")

    # Act
    with pytest.raises(NomeDeEspacoJaCadastrado):
        repositorio.salvar(renomeado)

    # Assert
    assert repositorio.obter_por_id(outro.id).nome == "Ginásio B"


def _duas_leituras(repositorio):
    espaco_id = repositorio.salvar(novo_espaco()).id
    return repositorio.obter_por_id(espaco_id), repositorio.obter_por_id(espaco_id)


def test_edicao_sobre_leitura_anterior_a_uma_desativacao_e_recusada(repositorio):
    # Arrange
    desativacao, edicao = _duas_leituras(repositorio)
    desativacao.desativar()
    repositorio.salvar(desativacao)
    edicao.alterar_dados(capacidade=99)

    # Act
    with pytest.raises(EspacoDesatualizado):
        repositorio.salvar(edicao)

    # Assert
    guardado = repositorio.obter_por_id(edicao.id)
    assert (guardado.capacidade, guardado.ativo) == (20, False)


def test_edicao_de_outro_campo_sobre_leitura_desatualizada_nao_apaga_a_primeira(
    repositorio,
):
    # Arrange
    primeira, segunda = _duas_leituras(repositorio)
    primeira.alterar_dados(nome="Quadra Reformada")
    repositorio.salvar(primeira)
    segunda.alterar_dados(capacidade=99)

    # Act
    with pytest.raises(EspacoDesatualizado):
        repositorio.salvar(segunda)

    # Assert
    guardado = repositorio.obter_por_id(primeira.id)
    assert (guardado.nome, guardado.capacidade) == ("Quadra Reformada", 20)


def test_salvar_de_novo_o_mesmo_objeto_nao_acusa_desatualizado(repositorio):
    # Arrange
    espaco = repositorio.obter_por_id(repositorio.salvar(novo_espaco()).id)
    espaco.alterar_dados(capacidade=30)
    repositorio.salvar(espaco)
    espaco.alterar_dados(capacidade=40)

    # Act
    repositorio.salvar(espaco)

    # Assert
    assert repositorio.obter_por_id(espaco.id).capacidade == 40


@pytest.mark.django_db
def test_salvar_espaco_existente_bloqueia_a_linha():
    # Arrange
    repositorio = RepositorioEspacosDjango()
    espaco = repositorio.obter_por_id(repositorio.salvar(novo_espaco()).id)
    espaco.alterar_dados(capacidade=30)

    # Act
    with CaptureQueriesContext(connection) as consultas:
        repositorio.salvar(espaco)

    # Assert
    assert any(
        'FROM "espacos_espaco_esportivo"' in consulta["sql"]
        and "FOR UPDATE" in consulta["sql"]
        for consulta in consultas.captured_queries
    )


def test_listar_ordena_por_nome(repositorio):
    # Arrange
    _salvar_espacos_para_listagem(repositorio)

    # Act
    espacos = repositorio.listar()

    # Assert
    assert nomes(espacos) == [
        "Campo Norte",
        "Ginasio Antigo",
        "Ginasio Novo",
        "Quadra Coberta",
    ]


@pytest.mark.parametrize(
    ("filtros", "nomes_esperados"),
    [
        ({"apenas_ativos": True}, ["Campo Norte", "Ginasio Novo", "Quadra Coberta"]),
        ({"tipo": TipoEspaco.GINASIO}, ["Ginasio Antigo", "Ginasio Novo"]),
        ({"apenas_ativos": True, "tipo": TipoEspaco.GINASIO}, ["Ginasio Novo"]),
        ({"tipo": TipoEspaco.QUADRA_DE_TENIS}, []),
    ],
    ids=["apenas-ativos", "por-tipo", "ativos-e-tipo", "tipo-sem-espacos"],
)
def test_listar_aplica_os_filtros(repositorio, filtros, nomes_esperados):
    # Arrange
    _salvar_espacos_para_listagem(repositorio)

    # Act
    espacos = repositorio.listar(**filtros)

    # Assert
    assert nomes(espacos) == nomes_esperados


@pytest.mark.parametrize(
    "alterar_fora_do_repositorio",
    [
        lambda repositorio, salvo: repositorio.obter_por_id(salvo.id).alterar_dados(
            capacidade=99
        ),
        lambda repositorio, salvo: repositorio.listar()[0].desativar(),
        lambda repositorio, salvo: salvo.alterar_dados(nome="Nome alterado fora"),
    ],
    ids=["obtida", "listada", "devolvida-ao-salvar"],
)
def test_alterar_entidade_devolvida_nao_altera_o_repositorio(
    repositorio, alterar_fora_do_repositorio
):
    # Arrange
    salvo = repositorio.salvar(novo_espaco())

    # Act
    alterar_fora_do_repositorio(repositorio, salvo)

    # Assert
    guardado = repositorio.obter_por_id(salvo.id)
    assert (guardado.nome, guardado.capacidade, guardado.ativo) == (
        "Quadra Central",
        20,
        True,
    )


@pytest.mark.parametrize(
    ("nome", "existe"),
    [("GINÁSIO a", True), ("Ginásio B", False)],
    ids=["mesmo-nome-com-outra-caixa", "nome-de-nenhum-espaco"],
)
def test_existe_com_nome_nao_diferencia_caixa(repositorio, nome, existe):
    # Arrange
    repositorio.salvar(novo_espaco(nome="Ginásio A"))

    # Act
    resultado = repositorio.existe_com_nome(nome)

    # Assert
    assert resultado is existe


@pytest.mark.parametrize(
    ("ignorado", "existe"),
    [("o-dono-do-nome", False), ("outro-espaco", True)],
)
def test_existe_com_nome_ignora_apenas_o_id_informado(repositorio, ignorado, existe):
    # Arrange
    dono = repositorio.salvar(novo_espaco(nome="Ginásio A"))
    outro = repositorio.salvar(novo_espaco(nome="Ginásio B"))
    ignorar_id = {"o-dono-do-nome": dono.id, "outro-espaco": outro.id}[ignorado]

    # Act
    resultado = repositorio.existe_com_nome("ginásio a", ignorar_id=ignorar_id)

    # Assert
    assert resultado is existe


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("campos", "constraint"),
    [
        ({"capacidade": 0}, "espacos_espaco_esportivo_capacidade_minima"),
        ({"tipo": "PISCINA"}, "espacos_espaco_esportivo_tipo_valido"),
    ],
    ids=["capacidade-zero", "tipo-desconhecido"],
)
def test_banco_recusa_dados_que_a_entidade_nao_aceitaria(campos, constraint):
    # Arrange
    dados = {"nome": "Quadra", "tipo": TipoEspaco.GINASIO.value, "capacidade": 10}
    dados.update(campos)

    # Act / Assert
    with pytest.raises(IntegrityError, match=constraint):
        EspacoEsportivoModel.objects.create(**dados)


@pytest.mark.django_db
def test_salvar_repassa_integrity_error_que_nao_e_de_nome_repetido():
    # Arrange
    espaco = novo_espaco()
    espaco._capacidade = 0

    # Act / Assert
    with pytest.raises(IntegrityError, match="capacidade_minima"):
        RepositorioEspacosDjango().salvar(espaco)


def test_model_mostra_o_nome_do_espaco():
    # Act
    texto = str(EspacoEsportivoModel(nome="Quadra Central"))

    # Assert
    assert texto == "Quadra Central"
