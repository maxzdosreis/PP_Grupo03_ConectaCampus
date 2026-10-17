import pytest
from django.db import IntegrityError

from contas.domain.perfil import PerfilUsuario
from contas.infrastructure.models import Usuario

SENHA = "senha-de-teste-123"


def _dados(**alteracoes):
    dados = {"email": "ana@x.com", "nome": "Ana Souza", "matricula": "2026001"}
    dados.update(alteracoes)
    return dados


@pytest.mark.django_db
def test_create_user_normaliza_email_e_cria_solicitante():
    # Arrange
    dados = _dados(email="  Ana@X.com ", nome=" Ana Souza ", matricula=" 2026001 ")

    # Act
    usuario = Usuario.objects.create_user(senha=SENHA, **dados)

    # Assert
    assert usuario.email == "ana@x.com"
    assert usuario.nome == "Ana Souza"
    assert usuario.matricula == "2026001"
    assert usuario.perfil == PerfilUsuario.SOLICITANTE
    assert not usuario.is_staff
    assert not usuario.is_superuser


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("campo", "valor", "mensagem"),
    [
        ("email", "", "Informe o e-mail."),
        ("email", "   ", "Informe o e-mail."),
        ("nome", None, "Informe o nome."),
        ("nome", "  ", "Informe o nome."),
        ("matricula", None, "Informe a matrícula."),
        ("matricula", "  ", "Informe a matrícula."),
    ],
)
def test_create_user_sem_campo_obrigatorio_lanca_erro_em_portugues(
    campo, valor, mensagem
):
    # Arrange
    dados = _dados(**{campo: valor})

    # Act / Assert
    with pytest.raises(ValueError, match=mensagem):
        Usuario.objects.create_user(senha=SENHA, **dados)
    assert not Usuario.objects.exists()


@pytest.mark.django_db
def test_create_superuser_cria_gestor_com_staff_e_superuser():
    # Arrange
    dados = _dados()

    # Act
    usuario = Usuario.objects.create_superuser(password=SENHA, **dados)

    # Assert
    assert usuario.perfil == PerfilUsuario.GESTOR
    assert usuario.is_staff
    assert usuario.is_superuser


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("campo", "valor"),
    [
        ("is_staff", False),
        ("is_superuser", False),
        ("perfil", PerfilUsuario.SOLICITANTE),
    ],
)
def test_create_superuser_recusa_valores_contraditorios(campo, valor):
    # Arrange
    dados = _dados(**{campo: valor})

    # Act / Assert
    with pytest.raises(ValueError, match="O superusuário precisa ter"):
        Usuario.objects.create_superuser(password=SENHA, **dados)
    assert not Usuario.objects.exists()


@pytest.mark.django_db
def test_email_repetido_com_caixa_diferente_viola_unicidade():
    # Arrange
    Usuario.objects.create_user(senha=SENHA, **_dados(email="ana@x.com"))

    # Act / Assert: grava direto pelo ORM, sem a normalização do manager,
    # para provar que o próprio banco recusa a mesma caixa-baixa.
    with pytest.raises(IntegrityError, match="contas_usuario_email_unico_sem_caixa"):
        Usuario.objects.create(**_dados(email="Ana@x.com", matricula="2026002"))


@pytest.mark.django_db
def test_matricula_repetida_viola_unicidade():
    # Arrange
    Usuario.objects.create_user(senha=SENHA, **_dados())

    # Act / Assert
    with pytest.raises(IntegrityError):
        Usuario.objects.create_user(senha=SENHA, **_dados(email="outra@x.com"))


@pytest.mark.django_db
def test_senha_nao_e_gravada_em_texto_puro():
    # Arrange
    dados = _dados()

    # Act
    usuario = Usuario.objects.create_user(senha=SENHA, **dados)
    usuario.refresh_from_db()

    # Assert
    assert SENHA not in usuario.password
    assert usuario.check_password(SENHA)
