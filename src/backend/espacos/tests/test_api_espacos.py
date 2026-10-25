import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from espacos.domain.espaco_esportivo import EspacoEsportivo
from espacos.domain.tipo_espaco import TipoEspaco
from espacos.infrastructure.repositorio_django import RepositorioEspacosDjango

pytestmark = pytest.mark.django_db

URL_LISTA = reverse("espacos:lista")
URL_TIPOS = reverse("espacos:tipos")
ID_INEXISTENTE = 9999


@pytest.fixture
def cliente():
    return APIClient()


def _url_detalhe(espaco_id):
    return reverse("espacos:detalhe", args=[espaco_id])


def _dados_validos(**sobrescritas):
    dados = {"nome": "Ginásio A", "tipo": "GINASIO", "capacidade": 50}
    dados.update(sobrescritas)
    return dados


def _cadastrar(cliente, **sobrescritas):
    return cliente.post(URL_LISTA, _dados_validos(**sobrescritas), format="json")


def _listar(cliente, **filtros):
    return cliente.get(URL_LISTA, filtros)


def _nomes(resposta):
    return [espaco["nome"] for espaco in resposta.data["dados"]]


def _cadastrar_espacos_para_listagem(cliente):
    _cadastrar(cliente, nome="Quadra Coberta", tipo="QUADRA_POLIESPORTIVA")
    _cadastrar(cliente, nome="Ginásio Novo", tipo="GINASIO")
    _cadastrar(cliente, nome="Campo Norte", tipo="CAMPO_DE_FUTEBOL")
    # Ainda não há endpoint para desativar (ESP-04): o inativo vai pelo repositório.
    RepositorioEspacosDjango().salvar(
        EspacoEsportivo(
            nome="Ginásio Antigo", tipo=TipoEspaco.GINASIO, capacidade=10, ativo=False
        )
    )


def test_cadastrar_espaco_valido_responde_201_com_o_espaco(cliente):
    # Act
    resposta = _cadastrar(cliente, nome="  Ginásio   Central ")

    # Assert
    assert resposta.status_code == 201
    assert set(resposta.data) == {"mensagem", "dados"}
    assert resposta.data["mensagem"] == "Espaço cadastrado com sucesso."
    dados = resposta.data["dados"]
    assert isinstance(dados["id"], int)
    assert dados == {
        "id": dados["id"],
        "nome": "Ginásio Central",
        "tipo": "GINASIO",
        "tipo_rotulo": "Ginásio",
        "capacidade": 50,
        "ativo": True,
    }


def test_cadastrar_aceita_capacidade_numerica_em_texto(cliente):
    # Act
    resposta = _cadastrar(cliente, capacidade="10")

    # Assert
    assert resposta.status_code == 201
    assert resposta.data["dados"]["capacidade"] == 10


def test_espaco_cadastrado_aparece_na_listagem(cliente):
    # Act
    _cadastrar(cliente)

    # Assert
    assert _nomes(_listar(cliente)) == ["Ginásio A"]


@pytest.mark.parametrize(
    ("corpo", "status", "codigo", "campo"),
    [
        (
            {"tipo": "GINASIO", "capacidade": 10},
            400,
            "DADOS_INVALIDOS",
            "nome",
        ),
        (_dados_validos(nome="   "), 400, "CAMPO_OBRIGATORIO_AUSENTE", "nome"),
        (_dados_validos(tipo=""), 400, "CAMPO_OBRIGATORIO_AUSENTE", "tipo"),
        (_dados_validos(capacidade="abc"), 400, "DADOS_INVALIDOS", "capacidade"),
        (_dados_validos(capacidade=0), 400, "CAPACIDADE_INVALIDA", "capacidade"),
        (
            _dados_validos(capacidade=99_999_999_999),
            400,
            "DADOS_INVALIDOS",
            "capacidade",
        ),
        (
            _dados_validos(nome="Quadra " + "x" * 100),
            400,
            "NOME_DE_ESPACO_MUITO_LONGO",
            "nome",
        ),
        (_dados_validos(tipo="PISCINA"), 400, "TIPO_DE_ESPACO_INVALIDO", "tipo"),
        (
            _dados_validos(nome="  GINÁSIO   a "),
            409,
            "NOME_DE_ESPACO_JA_CADASTRADO",
            "nome",
        ),
    ],
    ids=[
        "sem-nome",
        "nome-so-com-espacos",
        "tipo-vazio",
        "capacidade-texto",
        "capacidade-zero",
        "capacidade-acima-do-banco",
        "nome-longo",
        "tipo-desconhecido",
        "nome-repetido",
    ],
)
def test_cadastro_invalido_responde_erro_e_preserva_a_listagem(
    cliente, corpo, status, codigo, campo
):
    # Arrange
    _cadastrar(cliente, nome="Ginásio A")
    listagem_antes = _listar(cliente).data

    # Act
    resposta = cliente.post(URL_LISTA, corpo, format="json")

    # Assert
    assert resposta.status_code == status
    assert resposta.data["erro"]["codigo"] == codigo
    assert campo in resposta.data["erro"]["campos"]
    assert _listar(cliente).data == listagem_antes


def test_corpo_que_nao_e_json_responde_json_invalido(cliente):
    # Act
    resposta = cliente.post(URL_LISTA, data="{nome:", content_type="application/json")

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "JSON_INVALIDO"
    assert _listar(cliente).data["dados"] == []


def test_listar_ordena_por_nome(cliente):
    # Arrange
    _cadastrar_espacos_para_listagem(cliente)

    # Act
    resposta = _listar(cliente)

    # Assert
    assert resposta.status_code == 200
    assert _nomes(resposta) == [
        "Campo Norte",
        "Ginásio Antigo",
        "Ginásio Novo",
        "Quadra Coberta",
    ]


@pytest.mark.parametrize(
    ("filtros", "nomes_esperados"),
    [
        ({"apenas_ativos": "true"}, ["Campo Norte", "Ginásio Novo", "Quadra Coberta"]),
        ({"tipo": "GINASIO"}, ["Ginásio Antigo", "Ginásio Novo"]),
        ({"apenas_ativos": "true", "tipo": "GINASIO"}, ["Ginásio Novo"]),
        (
            {"tipo": ""},
            ["Campo Norte", "Ginásio Antigo", "Ginásio Novo", "Quadra Coberta"],
        ),
    ],
    ids=["apenas-ativos", "por-tipo", "ativos-e-tipo", "tipo-vazio-sem-filtro"],
)
def test_listar_aplica_os_filtros_da_query_string(cliente, filtros, nomes_esperados):
    # Arrange
    _cadastrar_espacos_para_listagem(cliente)

    # Act
    resposta = _listar(cliente, **filtros)

    # Assert
    assert resposta.status_code == 200
    assert _nomes(resposta) == nomes_esperados


def test_listar_com_tipo_desconhecido_no_filtro_responde_400(cliente):
    # Act
    resposta = _listar(cliente, tipo="PISCINA")

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "DADOS_INVALIDOS"
    assert "tipo" in resposta.data["erro"]["campos"]


@pytest.mark.parametrize(
    ("quantidade", "mensagem"),
    [
        (0, "Nenhum espaço encontrado."),
        (1, "1 espaço encontrado."),
        (3, "3 espaços encontrados."),
    ],
)
def test_listar_informa_a_quantidade_encontrada(cliente, quantidade, mensagem):
    # Arrange
    for numero in range(quantidade):
        _cadastrar(cliente, nome=f"Quadra {numero}")

    # Act
    resposta = _listar(cliente)

    # Assert
    assert resposta.data["mensagem"] == mensagem
    assert len(resposta.data["dados"]) == quantidade


def test_obter_espaco_existente_responde_200_com_o_espaco(cliente):
    # Arrange
    cadastrado = _cadastrar(cliente).data["dados"]

    # Act
    resposta = cliente.get(_url_detalhe(cadastrado["id"]))

    # Assert
    assert resposta.status_code == 200
    assert resposta.data == {"mensagem": "Espaço encontrado.", "dados": cadastrado}


def test_obter_espaco_inexistente_responde_404(cliente):
    # Act
    resposta = cliente.get(_url_detalhe(ID_INEXISTENTE))

    # Assert
    assert resposta.status_code == 404
    assert resposta.data == {
        "erro": {
            "codigo": "ESPACO_NAO_ENCONTRADO",
            "mensagem": f"Espaço de código {ID_INEXISTENTE} não encontrado.",
        }
    }


def test_tipos_de_espaco_lista_todos_os_tipos_na_ordem_do_enum(cliente):
    # Act
    resposta = cliente.get(URL_TIPOS)

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Tipos de espaço disponíveis."
    assert resposta.data["dados"][0] == {
        "valor": "QUADRA_POLIESPORTIVA",
        "rotulo": "Quadra poliesportiva",
    }
    assert resposta.data["dados"] == [
        {"valor": tipo.value, "rotulo": tipo.rotulo} for tipo in TipoEspaco
    ]
