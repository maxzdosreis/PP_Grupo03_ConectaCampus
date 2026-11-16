import pytest

from compartilhado.domain.erros import CampoObrigatorioAusente
from contas.application.casos_de_uso import AlterarSenha, CadastrarSolicitante
from contas.domain.excecoes import (
    NovaSenhaIgualAAtual,
    SenhaAtualIncorreta,
    SenhaFraca,
)
from contas.tests.fakes import PoliticaDeSenhaFake, RepositorioUsuariosEmMemoria

SENHA_ATUAL = "Quadra-Azul-2026!"
SENHA_NOVA = "Rede-Alta-73-nova"
SENHA_FRACA = "fraca"


@pytest.fixture
def repositorio():
    return RepositorioUsuariosEmMemoria()


@pytest.fixture
def politica():
    return PoliticaDeSenhaFake(senhas_fracas=(SENHA_FRACA,))


@pytest.fixture
def usuario_id(repositorio, politica):
    usuario = CadastrarSolicitante(repositorio, politica).executar(
        nome="Ana Souza", matricula="2026001", email="ana@x.com", senha=SENHA_ATUAL
    )
    return usuario.id


@pytest.fixture
def alterar(repositorio, politica, usuario_id):
    caso_de_uso = AlterarSenha(repositorio, politica)

    def executar(**alteracoes):
        campos = {
            "usuario_id": usuario_id,
            "senha_atual": SENHA_ATUAL,
            "nova_senha": SENHA_NOVA,
        }
        campos.update(alteracoes)
        return caso_de_uso.executar(**campos)

    return executar


def test_troca_valida_passa_a_valer_a_nova_senha_e_nao_a_antiga(
    alterar, repositorio, usuario_id
):
    # Act
    alterar()

    # Assert
    assert repositorio.senha_confere(usuario_id, SENHA_NOVA)
    assert not repositorio.senha_confere(usuario_id, SENHA_ATUAL)


def test_nova_senha_com_espacos_nas_pontas_e_gravada_como_foi_digitada(
    alterar, repositorio, usuario_id
):
    # Act
    alterar(nova_senha=f"  {SENHA_NOVA}  ")

    # Assert
    assert repositorio.senhas[usuario_id] == f"  {SENHA_NOVA}  "


def test_senha_atual_errada_lanca_senha_atual_incorreta_sem_trocar(
    alterar, repositorio, usuario_id
):
    # Act / Assert
    with pytest.raises(SenhaAtualIncorreta) as erro:
        alterar(senha_atual="outra-senha-qualquer")
    assert erro.value.campo == "senha_atual"
    assert repositorio.senhas[usuario_id] == SENHA_ATUAL


def test_senha_atual_errada_e_informada_antes_da_politica(alterar):
    # Act / Assert
    with pytest.raises(SenhaAtualIncorreta):
        alterar(senha_atual="outra-senha-qualquer", nova_senha=SENHA_FRACA)


def test_nova_senha_igual_a_atual_lanca_nova_senha_igual_a_atual(
    alterar, repositorio, usuario_id
):
    # Act / Assert
    with pytest.raises(NovaSenhaIgualAAtual) as erro:
        alterar(nova_senha=SENHA_ATUAL)
    assert erro.value.campo == "nova_senha"
    assert repositorio.senhas[usuario_id] == SENHA_ATUAL


def test_nova_senha_fraca_lanca_senha_fraca_no_campo_da_nova_senha(
    alterar, repositorio, usuario_id
):
    # Act / Assert
    with pytest.raises(SenhaFraca) as erro:
        alterar(nova_senha=SENHA_FRACA)
    assert erro.value.campo == "nova_senha"
    assert erro.value.motivos == (PoliticaDeSenhaFake.MOTIVO,)
    assert repositorio.senhas[usuario_id] == SENHA_ATUAL


@pytest.mark.parametrize("senha_atual", ["", "        ", None])
def test_senha_atual_vazia_lanca_campo_obrigatorio_ausente(alterar, senha_atual):
    # Act / Assert
    with pytest.raises(CampoObrigatorioAusente) as erro:
        alterar(senha_atual=senha_atual)
    assert erro.value.campo == "senha_atual"


@pytest.mark.parametrize("nova_senha", ["", "        ", None])
def test_nova_senha_vazia_lanca_campo_obrigatorio_ausente(alterar, nova_senha):
    # Act / Assert
    with pytest.raises(CampoObrigatorioAusente) as erro:
        alterar(nova_senha=nova_senha)
    assert erro.value.campo == "nova_senha"
