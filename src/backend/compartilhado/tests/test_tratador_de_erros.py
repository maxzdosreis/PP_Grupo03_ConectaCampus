import logging

import pytest
from django.http import Http404
from rest_framework.exceptions import (
    MethodNotAllowed,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
    UnsupportedMediaType,
    ValidationError,
)

from compartilhado.api.tratador_de_erros import MENSAGEM_ERRO_GENERICO, tratar_excecao
from compartilhado.domain.erros import (
    AcaoNaoPermitida,
    CampoObrigatorioAusente,
    ConflitoDeEstado,
    DadosInvalidos,
    ErroDeDominio,
    RecursoNaoEncontrado,
)


class _CapacidadeInvalida(DadosInvalidos):
    codigo = "CAPACIDADE_INVALIDA"
    mensagem_padrao = "A capacidade deve ser maior que zero."


class _EspacoInexistente(RecursoNaoEncontrado):
    codigo = "ESPACO_INEXISTENTE"
    mensagem_padrao = "Espaço não encontrado."


class _HorarioOcupado(ConflitoDeEstado):
    codigo = "HORARIO_OCUPADO"
    mensagem_padrao = "Já existe reserva neste horário."


class _SoGestor(AcaoNaoPermitida):
    mensagem_padrao = "Só o gestor pode confirmar reservas."


class _SemCategoria(ErroDeDominio):
    codigo = "SEM_CATEGORIA"


def _erro(resposta):
    return resposta.data["erro"]


@pytest.mark.parametrize(
    ("excecao", "status"),
    [
        (_CapacidadeInvalida(), 400),
        (_EspacoInexistente(), 404),
        (_HorarioOcupado(), 409),
        (_SoGestor(), 403),
    ],
)
def test_erro_de_dominio_usa_o_status_da_categoria(excecao, status):
    # Act
    resposta = tratar_excecao(excecao, {})

    # Assert
    assert resposta.status_code == status
    assert resposta.data == {
        "erro": {"codigo": excecao.codigo, "mensagem": excecao.mensagem}
    }


def test_acao_nao_permitida_usa_o_codigo_acao_nao_permitida():
    # Act
    resposta = tratar_excecao(_SoGestor(), {})

    # Assert
    assert _erro(resposta)["codigo"] == "ACAO_NAO_PERMITIDA"
    assert _erro(resposta)["mensagem"] == "Só o gestor pode confirmar reservas."


def test_campo_obrigatorio_ausente_indica_o_campo_que_falhou():
    # Act
    resposta = tratar_excecao(CampoObrigatorioAusente("nome", "Nome"), {})

    # Assert
    assert resposta.status_code == 400
    assert resposta.data == {
        "erro": {
            "codigo": "CAMPO_OBRIGATORIO_AUSENTE",
            "mensagem": 'O campo "Nome" é obrigatório.',
            "campos": {"nome": ['O campo "Nome" é obrigatório.']},
        }
    }


def test_validation_error_por_campo_lista_as_mensagens_de_cada_campo():
    # Arrange
    excecao = ValidationError(
        {"nome": ["Este campo é obrigatório."], "capacidade": ["Informe um número."]}
    )

    # Act
    resposta = tratar_excecao(excecao, {})

    # Assert
    assert resposta.status_code == 400
    assert resposta.data == {
        "erro": {
            "codigo": "DADOS_INVALIDOS",
            "mensagem": "Verifique os dados informados.",
            "campos": {
                "nome": ["Este campo é obrigatório."],
                "capacidade": ["Informe um número."],
            },
        }
    }


@pytest.mark.parametrize(
    "detalhe",
    [
        {"non_field_errors": ["Informe a data ou o espaço."]},
        ["Informe a data ou o espaço."],
    ],
)
def test_validation_error_so_com_erro_geral_usa_ele_como_mensagem(detalhe):
    # Act
    resposta = tratar_excecao(ValidationError(detalhe), {})

    # Assert
    assert resposta.status_code == 400
    assert resposta.data == {
        "erro": {
            "codigo": "DADOS_INVALIDOS",
            "mensagem": "Informe a data ou o espaço.",
        }
    }


def test_validation_error_aninhado_e_achatado_no_campo_de_primeiro_nivel():
    # Arrange
    excecao = ValidationError({"solicitante": {"matricula": ["Obrigatória."]}})

    # Act
    resposta = tratar_excecao(excecao, {})

    # Assert
    assert _erro(resposta)["campos"] == {"solicitante": ["Obrigatória."]}


@pytest.mark.parametrize(
    ("excecao", "status", "codigo", "mensagem"),
    [
        (
            ParseError(),
            400,
            "JSON_INVALIDO",
            "O corpo da requisição não é um JSON válido.",
        ),
        (
            PermissionDenied(),
            403,
            "ACAO_NAO_PERMITIDA",
            "Você não tem permissão para realizar esta ação.",
        ),
        (
            Http404(),
            404,
            "NAO_ENCONTRADO",
            "O recurso solicitado não foi encontrado.",
        ),
        (
            MethodNotAllowed("POST"),
            405,
            "METODO_NAO_PERMITIDO",
            "Método não permitido para este endereço.",
        ),
    ],
)
def test_excecao_do_framework_vira_codigo_e_mensagem_em_portugues(
    excecao, status, codigo, mensagem
):
    # Act
    resposta = tratar_excecao(excecao, {})

    # Assert
    assert resposta.status_code == status
    assert resposta.data == {"erro": {"codigo": codigo, "mensagem": mensagem}}


def test_nao_autenticado_mantem_o_header_www_authenticate():
    excecao = NotAuthenticated()
    excecao.auth_header = 'Bearer realm="api"'

    # Act
    resposta = tratar_excecao(excecao, {})

    # Assert
    assert resposta.status_code == 401
    assert resposta.headers["WWW-Authenticate"] == 'Bearer realm="api"'
    assert resposta.data == {
        "erro": {"codigo": "NAO_AUTENTICADO", "mensagem": "Faça login para continuar."}
    }


def test_outra_api_exception_mantem_status_e_usa_default_code_em_maiusculas():
    # Act
    resposta = tratar_excecao(UnsupportedMediaType("text/plain"), {})

    # Assert
    assert resposta.status_code == 415
    assert _erro(resposta)["codigo"] == "UNSUPPORTED_MEDIA_TYPE"
    assert _erro(resposta)["mensagem"] == MENSAGEM_ERRO_GENERICO


def test_excecao_inesperada_vira_500_sem_detalhes_e_fica_no_log(caplog):
    # Arrange
    excecao = RuntimeError("senha do banco: segredo")

    # Act
    with caplog.at_level(logging.ERROR):
        resposta = tratar_excecao(excecao, {})

    # Assert
    assert resposta.status_code == 500
    assert resposta.data == {
        "erro": {
            "codigo": "ERRO_INTERNO",
            "mensagem": "Ocorreu um erro inesperado. Tente novamente.",
        }
    }
    assert "segredo" not in str(resposta.data)
    assert caplog.records[-1].exc_info[1] is excecao


def test_erro_de_dominio_sem_categoria_e_tratado_como_erro_interno(caplog):
    # Act
    with caplog.at_level(logging.ERROR):
        resposta = tratar_excecao(_SemCategoria(), {})

    # Assert
    assert resposta.status_code == 500
    assert _erro(resposta)["codigo"] == "ERRO_INTERNO"
    assert caplog.records
