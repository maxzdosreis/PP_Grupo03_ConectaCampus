from datetime import timedelta

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from contas.domain.perfil import PerfilUsuario
from contas.infrastructure.models import Usuario

pytestmark = pytest.mark.django_db

URL_LOGIN = reverse("contas:login")
URL_REFRESH = reverse("contas:refresh")
URL_ME = reverse("contas:me")
EMAIL = "ana@x.com"
SENHA = "senha-de-teste-123"


@pytest.fixture
def usuario():
    return Usuario.objects.create_user(
        EMAIL, SENHA, nome="Ana Souza", matricula="2026001"
    )


def _login(email=EMAIL, senha=SENHA):
    return APIClient().post(URL_LOGIN, {"email": email, "senha": senha}, format="json")


def _tokens(resposta):
    return resposta.data["dados"]["access"], resposta.data["dados"]["refresh"]


def _me(access):
    cliente = APIClient()
    cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
    return cliente.get(URL_ME)


def _renovar(refresh):
    return APIClient().post(URL_REFRESH, {"refresh": refresh}, format="json")


def _assert_nao_autenticado(resposta):
    assert resposta.status_code == 401
    assert resposta.data["erro"]["codigo"] == "NAO_AUTENTICADO"
    assert resposta["WWW-Authenticate"].startswith("Bearer")


def test_login_valido_devolve_tokens_e_usuario_sem_senha(usuario):
    # Act
    resposta = _login()

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Login realizado com sucesso."
    dados = resposta.data["dados"]
    assert dados["access"]
    assert dados["refresh"]
    assert dados["usuario"] == {
        "id": usuario.pk,
        "nome": "Ana Souza",
        "email": EMAIL,
        "matricula": "2026001",
        "perfil": "SOLICITANTE",
        "perfil_rotulo": "Solicitante",
        "eh_gestor": False,
    }
    assert usuario.password not in str(resposta.data)


def test_login_aceita_email_com_caixa_diferente_e_espacos(usuario):
    # Act
    resposta = _login(email="  ANA@X.com ")

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"]["usuario"]["id"] == usuario.pk


def test_login_preenche_last_login(usuario):
    # Arrange
    assert usuario.last_login is None

    # Act
    _login()

    # Assert
    usuario.refresh_from_db()
    assert usuario.last_login is not None


def test_senha_errada_email_inexistente_e_inativo_respondem_igual(usuario):
    # Arrange
    Usuario.objects.create_user(
        "inativo@x.com", SENHA, nome="Bruno Lima", matricula="2026002", is_active=False
    )

    # Act
    respostas = [
        _login(senha="senha-errada"),
        _login(email="ninguem@x.com"),
        _login(email="inativo@x.com"),
    ]

    # Assert
    for resposta in respostas:
        assert resposta.status_code == 401
        assert resposta["WWW-Authenticate"].startswith("Bearer")
    assert respostas[0].data == {
        "erro": {
            "codigo": "CREDENCIAIS_INVALIDAS",
            "mensagem": "E-mail ou senha incorretos.",
        }
    }
    assert respostas[0].data == respostas[1].data == respostas[2].data


def test_login_sem_campos_responde_400_com_cada_campo():
    # Act
    resposta = APIClient().post(URL_LOGIN, {}, format="json")

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "DADOS_INVALIDOS"
    assert set(resposta.data["erro"]["campos"]) == {"email", "senha"}


def test_me_com_bearer_valido_devolve_usuario_com_perfil(usuario):
    # Arrange
    usuario.perfil = PerfilUsuario.GESTOR
    usuario.save()
    access, _ = _tokens(_login())

    # Act
    resposta = _me(access)

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Usuário autenticado."
    assert resposta.data["dados"]["perfil"] == "GESTOR"
    assert resposta.data["dados"]["perfil_rotulo"] == "Gestor"
    assert resposta.data["dados"]["eh_gestor"] is True


def test_me_sem_token_responde_401_com_cabecalho_bearer():
    # Act
    resposta = APIClient().get(URL_ME)

    # Assert
    _assert_nao_autenticado(resposta)


def test_me_com_token_malformado_responde_401():
    # Act
    resposta = _me("isto-nao-e-um-token")

    # Assert
    _assert_nao_autenticado(resposta)


def test_me_com_access_expirado_responde_401(usuario):
    # Arrange
    access = AccessToken.for_user(usuario)
    access.set_exp(lifetime=-timedelta(minutes=1))

    # Act
    resposta = _me(str(access))

    # Assert
    _assert_nao_autenticado(resposta)


def test_access_dura_o_tempo_configurado(usuario):
    # Arrange
    access, _ = _tokens(_login())

    # Act
    token = AccessToken(access)

    # Assert
    assert token["exp"] - token["iat"] == timedelta(minutes=30).total_seconds()


def test_refresh_valido_devolve_access_novo_que_funciona_no_me(usuario):
    # Arrange
    _, refresh = _tokens(_login())

    # Act
    resposta = _renovar(refresh)

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Token renovado."
    assert set(resposta.data["dados"]) == {"access"}
    assert _me(resposta.data["dados"]["access"]).status_code == 200


def test_refresh_invalido_responde_401_no_formato_padrao():
    # Act
    resposta = _renovar("isto-nao-e-um-token")

    # Assert
    _assert_nao_autenticado(resposta)
    assert resposta.data == {
        "erro": {"codigo": "NAO_AUTENTICADO", "mensagem": "Faça login para continuar."}
    }


def test_access_usado_como_refresh_responde_401(usuario):
    # Arrange
    access, _ = _tokens(_login())

    # Act
    resposta = _renovar(access)

    # Assert
    _assert_nao_autenticado(resposta)


def test_refresh_sem_campo_responde_400():
    # Act
    resposta = APIClient().post(URL_REFRESH, {}, format="json")

    # Assert
    assert resposta.status_code == 400
    assert "refresh" in resposta.data["erro"]["campos"]
