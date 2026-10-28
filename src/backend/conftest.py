import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

SENHA_DE_TESTE = "senha-de-teste-123"


def _cliente_de(usuario):
    cliente = APIClient()
    cliente.force_authenticate(user=usuario)
    return cliente


@pytest.fixture
def usuario_gestor(db):
    return get_user_model().objects.create_superuser(
        "gestora@teste.com", SENHA_DE_TESTE, nome="Gestora de Teste", matricula="G0001"
    )


@pytest.fixture
def usuario_solicitante(db):
    return get_user_model().objects.create_user(
        "ana@exemplo.com", SENHA_DE_TESTE, nome="Ana Souza", matricula="2026001"
    )


@pytest.fixture
def outro_solicitante(db):
    return get_user_model().objects.create_user(
        "bruno@exemplo.com", SENHA_DE_TESTE, nome="Bruno Lima", matricula="2026002"
    )


@pytest.fixture
def cliente_gestor(usuario_gestor):
    return _cliente_de(usuario_gestor)


@pytest.fixture
def cliente_solicitante(usuario_solicitante):
    return _cliente_de(usuario_solicitante)


@pytest.fixture
def tokens_de(db):
    def _tokens_de(usuario):
        resposta = APIClient().post(
            reverse("contas:login"),
            {"email": usuario.email, "senha": SENHA_DE_TESTE},
            format="json",
        )
        assert resposta.status_code == 200
        dados = resposta.data["dados"]
        return {"access": dados["access"], "refresh": dados["refresh"]}

    return _tokens_de


@pytest.fixture
def cliente_com_token(tokens_de):
    def _cliente_com_token(usuario):
        cliente = APIClient()
        access = tokens_de(usuario)["access"]
        cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        return cliente

    return _cliente_com_token


@pytest.fixture
def espaco_id(cliente_gestor):
    resposta = cliente_gestor.post(
        reverse("espacos:lista"),
        {"nome": "Quadra Coberta", "tipo": "QUADRA_POLIESPORTIVA", "capacidade": 20},
        format="json",
    )
    return resposta.data["dados"]["id"]
