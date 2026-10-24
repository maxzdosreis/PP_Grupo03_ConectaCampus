from dataclasses import FrozenInstanceError

import pytest

from compartilhado.domain.erros import CampoObrigatorioAusente, TextoMuitoLongo
from contas.domain.cadastro import (
    MATRICULA_MAXIMO_CARACTERES,
    NOME_MAXIMO_CARACTERES,
    DadosDeCadastro,
    normalizar_email,
    normalizar_nome,
)
from contas.domain.excecoes import MatriculaInvalida, SenhaFraca


def _dados(**alteracoes):
    campos = {"nome": "Ana Souza", "matricula": "2026001", "email": "ana@x.com"}
    campos.update(alteracoes)
    return DadosDeCadastro(**campos)


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("  Ana@Exemplo.COM ", "ana@exemplo.com"),
        ("ana@x.com", "ana@x.com"),
        (None, ""),
    ],
)
def test_normalizar_email_tira_espacos_das_pontas_e_usa_minusculas(entrada, esperado):
    # Act / Assert
    assert normalizar_email(entrada) == esperado


@pytest.mark.parametrize(
    ("entrada", "esperado"),
    [
        ("  Ana   Maria  Souza ", "Ana Maria Souza"),
        ("Ana\tSouza", "Ana Souza"),
        (None, ""),
    ],
)
def test_normalizar_nome_tira_espacos_das_pontas_e_repetidos(entrada, esperado):
    # Act / Assert
    assert normalizar_nome(entrada) == esperado


def test_dados_de_cadastro_normalizam_os_tres_campos():
    # Act
    dados = _dados(nome="  Ana   Souza ", matricula=" 2026001 ", email=" Ana@X.com ")

    # Assert
    assert dados.nome == "Ana Souza"
    assert dados.matricula == "2026001"
    assert dados.email == "ana@x.com"


def test_dados_de_cadastro_sao_imutaveis():
    # Arrange
    dados = _dados()

    # Act / Assert
    with pytest.raises(FrozenInstanceError):
        dados.nome = "Outro Nome"


@pytest.mark.parametrize("campo", ["nome", "matricula", "email"])
@pytest.mark.parametrize("valor", ["", "   ", None])
def test_campo_vazio_lanca_campo_obrigatorio_ausente(campo, valor):
    # Act / Assert
    with pytest.raises(CampoObrigatorioAusente) as erro:
        _dados(**{campo: valor})
    assert erro.value.campo == campo


def test_nome_no_limite_e_aceito():
    # Act
    dados = _dados(nome="a" * NOME_MAXIMO_CARACTERES)

    # Assert
    assert len(dados.nome) == 150


def test_nome_acima_do_limite_lanca_texto_muito_longo():
    # Act / Assert
    with pytest.raises(TextoMuitoLongo) as erro:
        _dados(nome="a" * (NOME_MAXIMO_CARACTERES + 1))
    assert erro.value.campo == "nome"
    assert str(erro.value) == 'O campo "Nome" deve ter no máximo 150 caracteres.'


def test_matricula_no_limite_e_aceita():
    # Act
    dados = _dados(matricula="1" * MATRICULA_MAXIMO_CARACTERES)

    # Assert
    assert len(dados.matricula) == 20


@pytest.mark.parametrize(
    "matricula", ["1" * (MATRICULA_MAXIMO_CARACTERES + 1), "2026 001", "2026\t001"]
)
def test_matricula_longa_ou_com_espaco_no_meio_lanca_matricula_invalida(matricula):
    # Act / Assert
    with pytest.raises(MatriculaInvalida) as erro:
        _dados(matricula=matricula)
    assert erro.value.campo == "matricula"
    assert erro.value.codigo == "MATRICULA_INVALIDA"
    assert str(erro.value) == (
        "A matrícula deve ter no máximo 20 caracteres e não pode conter espaços."
    )


def test_nome_invalido_e_informado_antes_da_matricula():
    # Act / Assert
    with pytest.raises(CampoObrigatorioAusente) as erro:
        _dados(nome="", matricula="com espaco")
    assert erro.value.campo == "nome"


def test_senha_fraca_junta_os_motivos_terminando_cada_um_com_ponto():
    # Act
    erro = SenhaFraca(
        ["Esta senha é muito comum.", "A senha é muito parecida com nome"]
    )

    # Assert
    assert erro.campo == "senha"
    assert erro.motivos == (
        "Esta senha é muito comum.",
        "A senha é muito parecida com nome",
    )
    assert str(erro) == "Esta senha é muito comum. A senha é muito parecida com nome."
