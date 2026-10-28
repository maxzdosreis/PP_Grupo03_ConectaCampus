import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from contas.domain.perfil import PerfilUsuario
from contas.infrastructure.models import Usuario

pytestmark = pytest.mark.django_db

URL_CADASTRO = reverse("contas:cadastro")
URL_LOGIN = reverse("contas:login")
SENHA = "Quadra-Azul-2026!"


def _corpo(**alteracoes):
    corpo = {
        "nome": "Ana Souza",
        "matricula": "2026001",
        "email": "ana@exemplo.com",
        "senha": SENHA,
    }
    corpo.update(alteracoes)
    return corpo


def _cadastrar(corpo=None, cliente=None):
    cliente = cliente or APIClient()
    corpo = _corpo() if corpo is None else corpo
    return cliente.post(URL_CADASTRO, corpo, format="json")


def _assert_erro(resposta, status, codigo, campo=None):
    assert resposta.status_code == status
    assert resposta.data["erro"]["codigo"] == codigo
    if campo:
        assert campo in resposta.data["erro"]["campos"]


def test_cadastro_valido_responde_201_com_solicitante_sem_senha():
    # Act
    resposta = _cadastrar(_corpo(email=" Ana@Exemplo.com "))

    # Assert
    assert resposta.status_code == 201
    assert resposta.data["mensagem"] == (
        "Cadastro realizado com sucesso. Faça login para continuar."
    )
    usuario = Usuario.objects.get()
    assert resposta.data["dados"] == {
        "id": usuario.pk,
        "nome": "Ana Souza",
        "email": "ana@exemplo.com",
        "matricula": "2026001",
        "perfil": "SOLICITANTE",
        "perfil_rotulo": "Solicitante",
        "eh_gestor": False,
    }


def test_campos_de_privilegio_no_corpo_sao_ignorados():
    # Act
    resposta = _cadastrar(_corpo(perfil="GESTOR", is_staff=True, is_superuser=True))

    # Assert
    assert resposta.status_code == 201
    assert resposta.data["dados"]["perfil"] == "SOLICITANTE"
    usuario = Usuario.objects.get()
    assert usuario.perfil == PerfilUsuario.SOLICITANTE
    assert not usuario.is_staff
    assert not usuario.is_superuser


def test_usuario_recem_cadastrado_consegue_fazer_login():
    # Arrange
    _cadastrar()

    # Act
    resposta = APIClient().post(
        URL_LOGIN, {"email": "ana@exemplo.com", "senha": SENHA}, format="json"
    )

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"]["usuario"]["perfil"] == "SOLICITANTE"


def test_senha_e_gravada_com_hash():
    # Act
    _cadastrar()

    # Assert
    usuario = Usuario.objects.get()
    assert usuario.password != SENHA
    assert usuario.check_password(SENHA)


def test_email_repetido_com_caixa_diferente_responde_409():
    # Arrange
    _cadastrar()

    # Act
    resposta = _cadastrar(_corpo(email="ANA@exemplo.com", matricula="2026002"))

    # Assert
    _assert_erro(resposta, 409, "EMAIL_JA_CADASTRADO", "email")
    assert resposta.data["erro"]["mensagem"] == "Já existe um usuário com este e-mail."
    assert Usuario.objects.count() == 1


def test_matricula_repetida_responde_409():
    # Arrange
    _cadastrar()

    # Act
    resposta = _cadastrar(_corpo(email="outra@exemplo.com"))

    # Assert
    _assert_erro(resposta, 409, "MATRICULA_JA_CADASTRADA", "matricula")
    assert Usuario.objects.count() == 1


def test_senha_fraca_responde_400_com_motivos_em_senha():
    # Act
    resposta = _cadastrar(_corpo(senha="12345678"))

    # Assert
    _assert_erro(resposta, 400, "SENHA_FRACA", "senha")
    assert resposta.data["erro"]["campos"]["senha"] == [
        "Esta senha é muito comum. Esta senha é inteiramente numérica."
    ]
    assert not Usuario.objects.exists()


def test_email_malformado_responde_400():
    # Act
    resposta = _cadastrar(_corpo(email="ana-sem-arroba"))

    # Assert
    _assert_erro(resposta, 400, "DADOS_INVALIDOS", "email")


def test_campos_ausentes_respondem_400_com_cada_campo():
    # Act
    resposta = _cadastrar({})

    # Assert
    _assert_erro(resposta, 400, "DADOS_INVALIDOS")
    assert set(resposta.data["erro"]["campos"]) == {
        "nome",
        "matricula",
        "email",
        "senha",
    }


def test_nome_so_com_espacos_responde_400_campo_obrigatorio():
    # Act
    resposta = _cadastrar(_corpo(nome="   "))

    # Assert
    _assert_erro(resposta, 400, "CAMPO_OBRIGATORIO_AUSENTE", "nome")


def test_matricula_com_espaco_responde_400():
    # Act
    resposta = _cadastrar(_corpo(matricula="2026 001"))

    # Assert
    _assert_erro(resposta, 400, "MATRICULA_INVALIDA", "matricula")


def test_header_authorization_invalido_nao_impede_o_cadastro():
    # Arrange
    cliente = APIClient()
    cliente.credentials(HTTP_AUTHORIZATION="Bearer token-invalido")

    # Act
    resposta = _cadastrar(cliente=cliente)

    # Assert
    assert resposta.status_code == 201
