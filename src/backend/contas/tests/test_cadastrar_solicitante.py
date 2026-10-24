import pytest

from compartilhado.domain.erros import CampoObrigatorioAusente
from contas.application.casos_de_uso import CadastrarSolicitante
from contas.domain.excecoes import EmailJaCadastrado, MatriculaJaCadastrada, SenhaFraca
from contas.domain.perfil import PerfilUsuario
from contas.tests.fakes import PoliticaDeSenhaFake, RepositorioUsuariosEmMemoria

SENHA_FORTE = "Quadra-Azul-2026!"
SENHA_FRACA = "fraca"


@pytest.fixture
def repositorio():
    return RepositorioUsuariosEmMemoria()


@pytest.fixture
def cadastrar(repositorio):
    caso_de_uso = CadastrarSolicitante(
        repositorio, PoliticaDeSenhaFake(senhas_fracas=(SENHA_FRACA,))
    )

    def executar(**alteracoes):
        campos = {
            "nome": "Ana Souza",
            "matricula": "2026001",
            "email": "ana@x.com",
            "senha": SENHA_FORTE,
        }
        campos.update(alteracoes)
        return caso_de_uso.executar(**campos)

    return executar


def test_cadastro_valido_cria_solicitante_com_dados_normalizados(
    cadastrar, repositorio
):
    # Act
    usuario = cadastrar(nome=" Ana   Souza ", email=" Ana@X.com ")

    # Assert
    assert usuario.id == 1
    assert usuario.nome == "Ana Souza"
    assert usuario.email == "ana@x.com"
    assert usuario.perfil == PerfilUsuario.SOLICITANTE
    assert repositorio.criados == {1: usuario}
    assert repositorio.senhas[1] == SENHA_FORTE


def test_email_repetido_com_caixa_diferente_lanca_email_ja_cadastrado(
    cadastrar, repositorio
):
    # Arrange
    cadastrar()

    # Act / Assert
    with pytest.raises(EmailJaCadastrado):
        cadastrar(email="ANA@x.com", matricula="2026002")
    assert len(repositorio.criados) == 1


def test_matricula_repetida_lanca_matricula_ja_cadastrada(cadastrar, repositorio):
    # Arrange
    cadastrar()

    # Act / Assert
    with pytest.raises(MatriculaJaCadastrada):
        cadastrar(email="outra@x.com")
    assert len(repositorio.criados) == 1


def test_senha_fraca_lanca_senha_fraca_sem_criar_usuario(cadastrar, repositorio):
    # Act / Assert
    with pytest.raises(SenhaFraca):
        cadastrar(senha=SENHA_FRACA)
    assert repositorio.criados == {}


@pytest.mark.parametrize("senha", ["", "        ", None])
def test_senha_vazia_ou_em_branco_lanca_campo_obrigatorio_ausente(
    cadastrar, repositorio, senha
):
    # Act / Assert
    with pytest.raises(CampoObrigatorioAusente) as erro:
        cadastrar(senha=senha)
    assert erro.value.campo == "senha"
    assert repositorio.criados == {}


def test_nome_vazio_e_informado_antes_da_senha_fraca(cadastrar):
    # Act / Assert
    with pytest.raises(CampoObrigatorioAusente) as erro:
        cadastrar(nome="  ", senha=SENHA_FRACA)
    assert erro.value.campo == "nome"


def test_senha_fraca_e_informada_antes_do_email_repetido(cadastrar):
    # Arrange
    cadastrar()

    # Act / Assert
    with pytest.raises(SenhaFraca):
        cadastrar(matricula="2026002", senha=SENHA_FRACA)
