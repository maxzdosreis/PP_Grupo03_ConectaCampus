"""Matriz de acesso da API, exercitada com JWT de verdade (AUT-07).

É a fonte da verdade de quem acessa cada rota. docs/fontes/matriz_de_acesso.md
repete esta tabela, e as duas mudam juntas. Toda rota ou método novo sob api/
precisa de uma linha aqui: a guarda de cobertura no fim do arquivo falha se faltar.
"""

import re
from datetime import timedelta
from typing import NamedTuple

import pytest
from django.contrib.auth import get_user_model
from django.urls import URLResolver, get_resolver, reverse
from django.utils import timezone
from rest_framework.test import APIClient

LIVRE = "não exige login"
PERSONAS = ("anonimo", "dono", "outro", "gestor")
METODOS_HTTP = ("GET", "POST", "PUT", "PATCH", "DELETE")
CODIGO_DO_ERRO = {
    401: "NAO_AUTENTICADO",
    403: "ACAO_NAO_PERMITIDA",
    405: "METODO_NAO_PERMITIDO",
}

EMAIL_DE_LOGIN = "carla@exemplo.com"
SENHA = "Quadra-Azul-2026!"


class Regra(NamedTuple):
    rota: str
    metodo: str
    corpo: str | None
    anonimo: int | str
    dono: int | str
    outro: int | str
    gestor: int | str


_TABELA = [
    ("health",             "GET",    None,                  200,   200,   200,   200),
    ("contas:login",       "POST",   "credenciais",         LIVRE, LIVRE, LIVRE, LIVRE),
    ("contas:refresh",     "POST",   "refresh",             LIVRE, LIVRE, LIVRE, LIVRE),
    ("contas:cadastro",    "POST",   "novo_usuario",        LIVRE, LIVRE, LIVRE, LIVRE),
    ("contas:me",          "GET",    None,                  401,   200,   200,   200),
    ("espacos:lista",      "GET",    None,                  401,   200,   200,   200),
    ("espacos:lista",      "POST",   "novo_espaco",         401,   403,   403,   201),
    ("espacos:tipos",      "GET",    None,                  200,   200,   200,   200),
    ("espacos:detalhe",    "GET",    None,                  401,   200,   200,   200),
    ("espacos:detalhe",    "DELETE", None,                  401,   405,   405,   405),
    ("reservas:lista",     "GET",    None,                  401,   200,   200,   200),
    ("reservas:lista",     "POST",   "nova_reserva",        401,   201,   201,   201),
    ("reservas:situacoes", "GET",    None,                  200,   200,   200,   200),
    ("reservas:detalhe",   "GET",    None,                  401,   200,   404,   200),
    ("reservas:detalhe",   "DELETE", None,                  401,   405,   405,   405),
    ("reservas:situacao",  "PATCH",  "confirmar",           401,   403,   404,   200),
    ("reservas:situacao",  "PATCH",  "cancelar_com_motivo", 401,   200,   404,   200),
]
# fmt: on
MATRIZ = [Regra(*linha) for linha in _TABELA]


class Cenario(NamedTuple):
    espaco_id: int
    reserva_id: int
    refresh: str


def _amanha():
    return (timezone.localdate() + timedelta(days=1)).isoformat()


def _reserva(espaco_id, hora_inicio, hora_fim):
    return {
        "espaco_id": espaco_id,
        "data": _amanha(),
        "hora_inicio": hora_inicio,
        "hora_fim": hora_fim,
        "finalidade": "Treino",
    }


CORPOS = {
    "credenciais": lambda cenario: {"email": EMAIL_DE_LOGIN, "senha": SENHA},
    "refresh": lambda cenario: {"refresh": cenario.refresh},
    "novo_usuario": lambda cenario: {
        "nome": "Davi Rocha",
        "matricula": "2026099",
        "email": "davi@exemplo.com",
        "senha": SENHA,
    },
    "novo_espaco": lambda cenario: {
        "nome": "Ginásio Novo",
        "tipo": "GINASIO",
        "capacidade": 30,
    },
    "nova_reserva": lambda cenario: _reserva(cenario.espaco_id, "14:00", "15:00"),
    "confirmar": lambda cenario: {"situacao": "CONFIRMADA"},
    "cancelar_com_motivo": lambda cenario: {
        "situacao": "CANCELADA",
        "motivo": "Não poderei comparecer",
    },
}


class Rota(NamedTuple):
    caminho: str
    view: object


def _rotas_da_api(padroes=None, prefixo="", namespace=""):
    rotas = {}
    for padrao in get_resolver().url_patterns if padroes is None else padroes:
        caminho = prefixo + str(padrao.pattern)
        if isinstance(padrao, URLResolver):
            interno = ":".join(filter(None, [namespace, padrao.namespace]))
            rotas.update(_rotas_da_api(padrao.url_patterns, caminho, interno))
        elif caminho.startswith("api/"):
            nome = ":".join(filter(None, [namespace, padrao.name]))
            rotas[nome if padrao.name else caminho] = Rota(caminho, padrao.callback)
    return rotas


def _metodos_implementados(view):
    return [metodo for metodo in METODOS_HTTP if hasattr(view.cls, metodo.lower())]


def _url(nome_da_rota, cenario):
    caminho = _rotas_da_api()[nome_da_rota].caminho
    parametros = re.findall(r"<(?:\w+:)?(\w+)>", caminho)
    return reverse(
        nome_da_rota, kwargs={nome: getattr(cenario, nome) for nome in parametros}
    )


def _requisitar(cliente, metodo, url, corpo):
    enviar = getattr(cliente, metodo.lower())
    if corpo is None:
        return enviar(url)
    return enviar(url, corpo, format="json")


@pytest.fixture(autouse=True)
def _hash_de_senha_rapido(settings):
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


@pytest.fixture
def cenario(cliente_com_token, tokens_de, usuario_gestor, usuario_solicitante):
    espaco_id = (
        cliente_com_token(usuario_gestor)
        .post(
            reverse("espacos:lista"),
            {"nome": "Quadra Coberta", "tipo": "GINASIO", "capacidade": 20},
            format="json",
        )
        .data["dados"]["id"]
    )
    reserva_id = (
        cliente_com_token(usuario_solicitante)
        .post(
            reverse("reservas:lista"),
            _reserva(espaco_id, "10:00", "11:00"),
            format="json",
        )
        .data["dados"]["id"]
    )
    get_user_model().objects.create_user(
        EMAIL_DE_LOGIN, SENHA, nome="Carla Dias", matricula="2026010"
    )
    return Cenario(espaco_id, reserva_id, tokens_de(usuario_solicitante)["refresh"])


@pytest.fixture
def cliente_da(
    cliente_com_token, usuario_solicitante, outro_solicitante, usuario_gestor
):
    usuarios = {
        "dono": usuario_solicitante,
        "outro": outro_solicitante,
        "gestor": usuario_gestor,
    }

    def _cliente_da(persona):
        if persona == "anonimo":
            return APIClient()
        return cliente_com_token(usuarios[persona])

    return _cliente_da


CASOS = [(regra, persona) for regra in MATRIZ for persona in PERSONAS]


def _id_do_caso(caso):
    regra, persona = caso
    partes = [regra.metodo, regra.rota, regra.corpo, persona]
    return "-".join(parte for parte in partes if parte)


@pytest.mark.parametrize(("regra", "persona"), CASOS, ids=map(_id_do_caso, CASOS))
def test_matriz_de_acesso(regra, persona, cenario, cliente_da):
    # Arrange
    esperado = getattr(regra, persona)
    corpo = CORPOS[regra.corpo](cenario) if regra.corpo else None

    # Act
    resposta = _requisitar(
        cliente_da(persona), regra.metodo, _url(regra.rota, cenario), corpo
    )

    # Assert
    descricao = f"{persona} em {regra.metodo} {regra.rota}"
    if esperado == LIVRE:
        assert resposta.status_code not in (401, 403), descricao
        return
    assert resposta.status_code == esperado, descricao
    if esperado in CODIGO_DO_ERRO:
        assert resposta.data["erro"]["codigo"] == CODIGO_DO_ERRO[esperado]


def test_toda_rota_da_api_tem_regra_de_acesso_na_matriz():
    # Arrange
    declaradas = {regra.rota for regra in MATRIZ}

    # Act
    faltando = [
        f"a rota {nome} ({rota.caminho}) não tem regra de acesso declarada na matriz"
        for nome, rota in _rotas_da_api().items()
        if nome not in declaradas
    ]

    # Assert
    assert not faltando, "\n".join(faltando)


def test_todo_metodo_implementado_tem_regra_de_acesso_na_matriz():
    # Arrange
    declarados = {(regra.rota, regra.metodo) for regra in MATRIZ}

    # Act
    faltando = [
        f"o método {metodo} da rota {nome} não tem regra de acesso declarada na matriz"
        for nome, rota in _rotas_da_api().items()
        for metodo in _metodos_implementados(rota.view)
        if (nome, metodo) not in declarados
    ]

    # Assert
    assert not faltando, "\n".join(faltando)


def test_toda_regra_da_matriz_aponta_para_uma_rota_existente():
    # Act
    inexistentes = {regra.rota for regra in MATRIZ} - set(_rotas_da_api())

    # Assert
    assert not inexistentes, f"rotas da matriz que não existem: {inexistentes}"
