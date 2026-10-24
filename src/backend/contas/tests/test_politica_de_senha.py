import pytest

from contas.domain.cadastro import DadosDeCadastro
from contas.domain.excecoes import SenhaFraca
from contas.infrastructure.politica_de_senha import PoliticaDeSenhaDjango

pytestmark = pytest.mark.django_db

DADOS = DadosDeCadastro(
    nome="Ana Souza", matricula="2026001", email="contato@exemplo.com"
)


def _motivos_da_recusa(senha, dados=DADOS):
    with pytest.raises(SenhaFraca) as erro:
        PoliticaDeSenhaDjango().validar(senha, dados)
    return erro.value.motivos


def test_senha_comum_e_numerica_e_recusada_com_mensagens_em_portugues():
    # Act
    motivos = _motivos_da_recusa("12345678")

    # Assert
    assert motivos == (
        "Esta senha é muito comum.",
        "Esta senha é inteiramente numérica.",
    )


@pytest.mark.parametrize(
    ("senha", "atributo"),
    [("contato@exemplo", "e-mail"), ("AnaSouza", "nome"), ("2026001x", "matrícula")],
)
def test_senha_parecida_com_os_dados_do_usuario_e_recusada(senha, atributo):
    # Act
    motivos = _motivos_da_recusa(senha)

    # Assert
    assert f"A senha é muito parecida com {atributo}" in motivos


def test_senha_com_sete_caracteres_e_recusada():
    # Act
    motivos = _motivos_da_recusa("Xq7#bLz")

    # Assert
    assert (
        "Esta senha é muito curta. Ela precisa conter pelo menos 8 caracteres."
        in motivos
    )


def test_senha_forte_e_aceita():
    # Act / Assert
    PoliticaDeSenhaDjango().validar("Quadra-Azul-2026!", DADOS)
