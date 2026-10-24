import pytest
from django.db import IntegrityError

from contas.domain.cadastro import DadosDeCadastro
from contas.domain.excecoes import EmailJaCadastrado, MatriculaJaCadastrada
from contas.domain.perfil import PerfilUsuario
from contas.infrastructure.models import Usuario
from contas.infrastructure.repositorio_django import RepositorioUsuariosDjango
from contas.tests.fakes import RepositorioUsuariosEmMemoria

SENHA = "Quadra-Azul-2026!"


@pytest.fixture(
    params=[
        pytest.param(
            RepositorioUsuariosDjango, marks=pytest.mark.django_db, id="django"
        ),
        pytest.param(RepositorioUsuariosEmMemoria, id="memoria"),
    ]
)
def repositorio(request):
    return request.param()


def _dados(**alteracoes):
    campos = {"nome": "Ana Souza", "matricula": "2026001", "email": "ana@x.com"}
    campos.update(alteracoes)
    return DadosDeCadastro(**campos)


def test_criar_solicitante_devolve_usuario_com_id_e_perfil_solicitante(repositorio):
    # Act
    usuario = repositorio.criar_solicitante(_dados(), SENHA)

    # Assert
    assert usuario.id is not None
    assert usuario.nome == "Ana Souza"
    assert usuario.email == "ana@x.com"
    assert usuario.matricula == "2026001"
    assert usuario.perfil == PerfilUsuario.SOLICITANTE


def test_existe_email_nao_diferencia_maiusculas(repositorio):
    # Arrange
    repositorio.criar_solicitante(_dados(), SENHA)

    # Act / Assert
    assert repositorio.existe_email("ANA@X.COM")
    assert not repositorio.existe_email("outra@x.com")


def test_existe_matricula(repositorio):
    # Arrange
    repositorio.criar_solicitante(_dados(), SENHA)

    # Act / Assert
    assert repositorio.existe_matricula("2026001")
    assert not repositorio.existe_matricula("2026002")


def test_email_repetido_lanca_email_ja_cadastrado(repositorio):
    # Arrange
    repositorio.criar_solicitante(_dados(), SENHA)

    # Act / Assert
    with pytest.raises(EmailJaCadastrado):
        repositorio.criar_solicitante(_dados(matricula="2026002"), SENHA)


def test_matricula_repetida_lanca_matricula_ja_cadastrada(repositorio):
    # Arrange
    repositorio.criar_solicitante(_dados(), SENHA)

    # Act / Assert
    with pytest.raises(MatriculaJaCadastrada):
        repositorio.criar_solicitante(_dados(email="outra@x.com"), SENHA)


@pytest.mark.django_db
def test_repositorio_django_grava_solicitante_comum_com_hash_da_senha():
    # Act
    cadastrado = RepositorioUsuariosDjango().criar_solicitante(_dados(), SENHA)

    # Assert
    usuario = Usuario.objects.get(pk=cadastrado.id)
    assert not usuario.is_staff
    assert not usuario.is_superuser
    assert usuario.password != SENHA
    assert usuario.check_password(SENHA)


@pytest.mark.django_db
def test_repositorio_django_relanca_integrity_error_de_outra_constraint(monkeypatch):
    # Arrange
    def falhar(*_args, **_kwargs):
        raise IntegrityError("outra constraint")

    monkeypatch.setattr(Usuario.objects, "create_user", falhar)

    # Act / Assert
    with pytest.raises(IntegrityError, match="outra constraint"):
        RepositorioUsuariosDjango().criar_solicitante(_dados(), SENHA)
