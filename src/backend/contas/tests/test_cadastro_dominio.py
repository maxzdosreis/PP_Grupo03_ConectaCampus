from dataclasses import FrozenInstanceError

import pytest
from hypothesis import given
from hypothesis import strategies as st

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


MENSAGEM_SO_DIGITOS = (
    "A matrícula deve ter só dígitos (0 a 9), sem letras, espaços nem símbolos."
)
MENSAGEM_LIMITE_TECNICO = "A matrícula pode ter no máximo 20 dígitos."


@pytest.mark.parametrize(
    ("entrada", "esperada"),
    [
        ("2026001", "2026001"),
        ("7", "7"),
        ("0", "0"),
        ("000123", "000123"),
        ("00123", "00123"),
        ("1" * MATRICULA_MAXIMO_CARACTERES, "1" * MATRICULA_MAXIMO_CARACTERES),
        ("  2026001 ", "2026001"),
        ("123\n", "123"),
    ],
)
def test_matricula_so_com_digitos_e_aceita_sem_minimo_e_com_zeros_a_esquerda(
    entrada, esperada
):
    # Act
    dados = _dados(matricula=entrada)

    # Assert
    assert dados.matricula == esperada
    assert isinstance(dados.matricula, str)


@pytest.mark.parametrize(
    "matricula",
    [
        "abc",
        "123a",
        "2026A01",
        "AB123",
        "2026 001",
        "2026\t001",
        "12\n34",
        "12.34",
        "12-34",
        "+123",
        "-123",
        "1e3",
        "٣٤٥",
        "１２３",
        "²",
        "①",
        "1" * 21 + "a",
    ],
)
def test_matricula_com_caractere_que_nao_e_digito_lanca_matricula_invalida(matricula):
    # Act / Assert
    with pytest.raises(MatriculaInvalida) as erro:
        _dados(matricula=matricula)
    assert erro.value.campo == "matricula"
    assert erro.value.codigo == "MATRICULA_INVALIDA"
    assert str(erro.value) == MENSAGEM_SO_DIGITOS


def test_unicode_que_o_python_chama_de_digito_nao_e_digito_de_matricula():
    # Arrange
    assert "٣٤٥".isdigit()
    assert "１２３".isdecimal()

    # Act / Assert
    for matricula in ("٣٤٥", "１２３"):
        with pytest.raises(MatriculaInvalida):
            _dados(matricula=matricula)


@pytest.mark.parametrize("quantidade", [MATRICULA_MAXIMO_CARACTERES + 1, 40])
def test_matricula_acima_do_limite_tecnico_lanca_matricula_invalida(quantidade):
    # Act / Assert
    with pytest.raises(MatriculaInvalida) as erro:
        _dados(matricula="1" * quantidade)
    assert erro.value.campo == "matricula"
    assert erro.value.codigo == "MATRICULA_INVALIDA"
    assert erro.value.limite == MATRICULA_MAXIMO_CARACTERES
    assert str(erro.value) == MENSAGEM_LIMITE_TECNICO


@pytest.mark.parametrize("matricula", ["", "   ", "\n"])
def test_matricula_vazia_lanca_campo_obrigatorio(matricula):
    # Act / Assert
    with pytest.raises(CampoObrigatorioAusente) as erro:
        _dados(matricula=matricula)
    assert erro.value.campo == "matricula"


@given(st.text(alphabet="0123456789", min_size=1, max_size=MATRICULA_MAXIMO_CARACTERES))
def test_propriedade_texto_de_1_a_20_digitos_e_matricula_valida(matricula):
    # Act / Assert
    assert _dados(matricula=matricula).matricula == matricula


@given(
    st.text(min_size=1, max_size=MATRICULA_MAXIMO_CARACTERES).filter(
        lambda texto: (
            texto.strip() != "" and not set(texto.strip()) <= set("0123456789")
        )
    )
)
def test_propriedade_texto_com_caractere_fora_de_0_a_9_e_recusado(matricula):
    # Act / Assert
    with pytest.raises(MatriculaInvalida):
        _dados(matricula=matricula)


@given(st.text(alphabet="0123456789", min_size=MATRICULA_MAXIMO_CARACTERES + 1))
def test_propriedade_mais_de_20_digitos_e_recusado(matricula):
    # Act / Assert
    with pytest.raises(MatriculaInvalida):
        _dados(matricula=matricula)


def test_nome_invalido_e_informado_antes_da_matricula():
    # Act / Assert
    with pytest.raises(CampoObrigatorioAusente) as erro:
        _dados(nome="", matricula="com letras")
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
