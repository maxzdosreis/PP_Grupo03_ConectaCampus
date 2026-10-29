import pytest
from django.db import IntegrityError

from espacos.domain.espaco_esportivo import EspacoEsportivo
from espacos.domain.excecoes import EspacoNaoEncontrado, NomeDeEspacoJaCadastrado
from espacos.domain.tipo_espaco import TipoEspaco
from espacos.infrastructure.models import EspacoEsportivoModel
from espacos.infrastructure.repositorio_django import RepositorioEspacosDjango
from espacos.tests.fakes import RepositorioEspacosEmMemoria

ID_INEXISTENTE = 9999


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


def _novo_espaco(**sobrescritas):
    dados = {
        "nome": "Quadra Central",
        "tipo": TipoEspaco.QUADRA_POLIESPORTIVA,
        "capacidade": 20,
    }
    dados.update(sobrescritas)
    return EspacoEsportivo(**dados)


def _salvar_espacos_para_listagem(repositorio):
    repositorio.salvar(_novo_espaco(nome="Quadra Coberta"))
    repositorio.salvar(
        _novo_espaco(nome="Ginasio Antigo", tipo=TipoEspaco.GINASIO, ativo=False)
    )
    repositorio.salvar(
        _novo_espaco(nome="Campo Norte", tipo=TipoEspaco.CAMPO_DE_FUTEBOL)
    )
    repositorio.salvar(_novo_espaco(nome="Ginasio Novo", tipo=TipoEspaco.GINASIO))


def _nomes(espacos):
    return [espaco.nome for espaco in espacos]


def test_salvar_espaco_novo_atribui_id_e_permite_obter_igual(repositorio):
    # Act
    salvo = repositorio.salvar(_novo_espaco(tipo=TipoEspaco.GINASIO))

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
    salvo = repositorio.salvar(_novo_espaco())
    alterado = _novo_espaco(
        id=salvo.id, nome="Quadra Reformada", capacidade=30, ativo=False
    )

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
    salvo = repositorio.salvar(_novo_espaco())

    # Act
    atualizado = repositorio.salvar(_novo_espaco(id=salvo.id, capacidade=40))

    # Assert
    assert atualizado.capacidade == 40
    assert repositorio.obter_por_id(salvo.id).capacidade == 40


def test_salvar_com_id_inexistente_lanca_espaco_nao_encontrado(repositorio):
    # Act
    with pytest.raises(EspacoNaoEncontrado) as erro:
        repositorio.salvar(_novo_espaco(id=ID_INEXISTENTE))

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
    repositorio.salvar(_novo_espaco(nome="Ginásio A"))

    # Act
    with pytest.raises(NomeDeEspacoJaCadastrado):
        repositorio.salvar(_novo_espaco(nome="ginásio a"))

    # Assert
    assert _nomes(repositorio.listar()) == ["Ginásio A"]


def test_renomear_para_o_nome_de_outro_espaco_lanca_nome_ja_cadastrado(repositorio):
    # Arrange
    repositorio.salvar(_novo_espaco(nome="Ginásio A"))
    outro = repositorio.salvar(_novo_espaco(nome="Ginásio B"))

    # Act
    with pytest.raises(NomeDeEspacoJaCadastrado):
        repositorio.salvar(_novo_espaco(id=outro.id, nome="GINÁSIO A"))

    # Assert
    assert repositorio.obter_por_id(outro.id).nome == "Ginásio B"


def test_listar_ordena_por_nome(repositorio):
    # Arrange
    _salvar_espacos_para_listagem(repositorio)

    # Act
    espacos = repositorio.listar()

    # Assert
    assert _nomes(espacos) == [
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
    assert _nomes(espacos) == nomes_esperados


def test_alterar_entidade_devolvida_nao_altera_o_repositorio(repositorio):
    # Arrange
    salvo = repositorio.salvar(_novo_espaco())

    # Act
    repositorio.obter_por_id(salvo.id).alterar_dados(capacidade=99)
    repositorio.listar()[0].desativar()
    salvo.alterar_dados(nome="Nome alterado fora do repositório")

    # Assert
    guardado = repositorio.obter_por_id(salvo.id)
    assert (guardado.nome, guardado.capacidade, guardado.ativo) == (
        "Quadra Central",
        20,
        True,
    )


def test_existe_com_nome_nao_diferencia_caixa(repositorio):
    # Arrange
    repositorio.salvar(_novo_espaco(nome="Ginásio A"))

    # Act / Assert
    assert repositorio.existe_com_nome("GINÁSIO a") is True
    assert repositorio.existe_com_nome("Ginásio B") is False


def test_existe_com_nome_ignora_apenas_o_id_informado(repositorio):
    # Arrange
    espaco = repositorio.salvar(_novo_espaco(nome="Ginásio A"))
    outro = repositorio.salvar(_novo_espaco(nome="Ginásio B"))

    # Act / Assert
    assert repositorio.existe_com_nome("ginásio a", ignorar_id=espaco.id) is False
    assert repositorio.existe_com_nome("ginásio a", ignorar_id=outro.id) is True


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
    espaco = _novo_espaco()
    espaco._capacidade = 0

    # Act / Assert
    with pytest.raises(IntegrityError, match="capacidade_minima"):
        RepositorioEspacosDjango().salvar(espaco)


def test_model_mostra_o_nome_do_espaco():
    # Act
    texto = str(EspacoEsportivoModel(nome="Quadra Central"))

    # Assert
    assert texto == "Quadra Central"
