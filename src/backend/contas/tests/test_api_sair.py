from datetime import timedelta

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from contas.infrastructure.models import Usuario

pytestmark = pytest.mark.django_db

URL_LOGIN = reverse("contas:login")
URL_REFRESH = reverse("contas:refresh")
URL_SAIR = reverse("contas:logout")
URL_ME = reverse("contas:me")
SENHA = "senha-de-teste-123"
SAIDA = {"mensagem": "Você saiu da sua conta.", "dados": None}


@pytest.fixture
def usuario():
    return Usuario.objects.create_user(
        "ana@x.com", SENHA, nome="Ana Souza", matricula="2026001"
    )


@pytest.fixture
def outro_usuario():
    return Usuario.objects.create_user(
        "bruno@x.com", SENHA, nome="Bruno Lima", matricula="2026002"
    )


def _tokens_de(usuario):
    resposta = APIClient().post(
        URL_LOGIN, {"email": usuario.email, "senha": SENHA}, format="json"
    )
    return resposta.data["dados"]["access"], resposta.data["dados"]["refresh"]


def _sair(corpo, cliente=None):
    return (cliente or APIClient()).post(URL_SAIR, corpo, format="json")


def _renovar(refresh):
    return APIClient().post(URL_REFRESH, {"refresh": refresh}, format="json")


def _com_access(access):
    cliente = APIClient()
    cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return cliente


def _assert_refresh_invalido(resposta):
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "DADOS_INVALIDOS"
    assert "refresh" in resposta.data["erro"]["campos"]


def test_sair_revoga_o_refresh_e_ele_deixa_de_renovar(usuario):
    # Arrange
    _, refresh = _tokens_de(usuario)

    # Act
    resposta = _sair({"refresh": refresh})

    # Assert
    assert resposta.status_code == 200
    assert resposta.data == SAIDA
    renovacao = _renovar(refresh)
    assert renovacao.status_code == 401
    assert renovacao.data["erro"]["codigo"] == "NAO_AUTENTICADO"


def test_sair_de_novo_com_o_mesmo_refresh_responde_200(usuario):
    # Arrange
    _, refresh = _tokens_de(usuario)
    _sair({"refresh": refresh})

    # Act
    resposta = _sair({"refresh": refresh})

    # Assert
    assert resposta.status_code == 200
    assert resposta.data == SAIDA
    assert BlacklistedToken.objects.count() == 1


def test_sair_com_refresh_vencido_responde_200_sem_revogar(usuario):
    # Arrange
    refresh = RefreshToken.for_user(usuario)
    refresh.set_exp(lifetime=-timedelta(minutes=1))

    # Act
    resposta = _sair({"refresh": str(refresh)})

    # Assert
    assert resposta.status_code == 200
    assert resposta.data == SAIDA
    assert not BlacklistedToken.objects.exists()


def test_sair_sem_refresh_responde_400_com_o_campo():
    # Act
    resposta = _sair({})

    # Assert
    _assert_refresh_invalido(resposta)


@pytest.mark.parametrize(
    "texto",
    ["", "isto-nao-e-um-token", "a.b.c"],
    ids=["vazio", "lixo", "tres-partes"],
)
def test_sair_com_texto_que_nao_e_token_responde_400_com_o_campo(texto):
    # Act
    resposta = _sair({"refresh": texto})

    # Assert
    _assert_refresh_invalido(resposta)


def test_sair_com_access_no_lugar_do_refresh_responde_400(usuario):
    # Arrange
    access, _ = _tokens_de(usuario)

    # Act
    resposta = _sair({"refresh": access})

    # Assert
    _assert_refresh_invalido(resposta)
    assert resposta.data["erro"]["campos"]["refresh"] == [
        "Informe um token de renovação válido."
    ]


def test_sair_com_access_vencido_no_cabecalho_funciona(usuario):
    # Arrange
    _, refresh = _tokens_de(usuario)
    access = AccessToken.for_user(usuario)
    access.set_exp(lifetime=-timedelta(minutes=1))

    # Act
    resposta = _sair({"refresh": refresh}, _com_access(str(access)))

    # Assert
    assert resposta.status_code == 200
    assert _renovar(refresh).status_code == 401


def test_access_emitido_antes_de_sair_continua_valendo_ate_expirar(usuario):
    # Arrange
    access, refresh = _tokens_de(usuario)

    # Act
    _sair({"refresh": refresh})

    # Assert
    assert _com_access(access).get(URL_ME).status_code == 200


def test_refresh_de_outra_pessoa_e_revogado_sem_dados_dela(usuario, outro_usuario):
    # Arrange
    access_da_ana, _ = _tokens_de(usuario)
    _, refresh_do_bruno = _tokens_de(outro_usuario)

    # Act
    resposta = _sair({"refresh": refresh_do_bruno}, _com_access(access_da_ana))

    # Assert
    assert resposta.data == SAIDA
    assert _renovar(refresh_do_bruno).status_code == 401


def test_refresh_emitido_antes_da_lista_negra_tambem_e_revogado(usuario):
    # Arrange: sem registro, como os emitidos antes da AUT-09
    _, refresh = _tokens_de(usuario)
    OutstandingToken.objects.all().delete()

    # Act
    resposta = _sair({"refresh": refresh})

    # Assert
    assert resposta.status_code == 200
    assert _renovar(refresh).status_code == 401
