import logging

from django.core.exceptions import PermissionDenied as PermissaoNegadaDoDjango
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.settings import api_settings
from rest_framework.views import exception_handler, set_rollback

from compartilhado.api.respostas import corpo_de_erro, resposta_erro
from compartilhado.domain.erros import (
    AcaoNaoPermitida,
    ConflitoDeEstado,
    DadosInvalidos,
    ErroDeDominio,
    RecursoNaoEncontrado,
)

logger = logging.getLogger(__name__)

MENSAGEM_ERRO_INTERNO = "Ocorreu um erro inesperado. Tente novamente."
MENSAGEM_ERRO_GENERICO = (
    "Não foi possível processar a requisição. Verifique os dados e tente novamente."
)

_STATUS_POR_CATEGORIA = {
    DadosInvalidos: status.HTTP_400_BAD_REQUEST,
    RecursoNaoEncontrado: status.HTTP_404_NOT_FOUND,
    ConflitoDeEstado: status.HTTP_409_CONFLICT,
    AcaoNaoPermitida: status.HTTP_403_FORBIDDEN,
}


def tratar_excecao(exc, context):
    if isinstance(exc, ErroDeDominio):
        return _responder_erro_de_dominio(exc, context)

    resposta = exception_handler(exc, context)
    if resposta is None:
        return _responder_erro_interno(exc, context)
    traduzir = _procurar_na_hierarquia(exc, _TRADUTORES, _traduzir_generico)
    resposta.data = traduzir(exc)
    return resposta


def _procurar_na_hierarquia(exc, tabela, padrao=None):
    for classe in type(exc).__mro__:
        if classe in tabela:
            return tabela[classe]
    return padrao


def _responder_erro_de_dominio(exc, context):
    status_http = _procurar_na_hierarquia(exc, _STATUS_POR_CATEGORIA)
    if status_http is None:
        # Herdar direto de ErroDeDominio, sem categoria, é erro de programação.
        return _responder_erro_interno(exc, context)
    set_rollback()
    campos = {exc.campo: [exc.mensagem]} if exc.campo else None
    return resposta_erro(exc.codigo, exc.mensagem, status_http, campos)


def _responder_erro_interno(exc, context):
    logger.exception("Erro inesperado em %s", context.get("view"), exc_info=exc)
    set_rollback()
    return resposta_erro(
        "ERRO_INTERNO", MENSAGEM_ERRO_INTERNO, status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def _traduzir_validacao(exc):
    chave_geral = api_settings.NON_FIELD_ERRORS_KEY
    erros = exc.detail if isinstance(exc.detail, dict) else {chave_geral: exc.detail}
    gerais = _mensagens(erros.get(chave_geral, []))
    campos = {
        campo: _mensagens(valor)
        for campo, valor in erros.items()
        if campo != chave_geral
    }
    mensagem = gerais[0] if gerais else DadosInvalidos.mensagem_padrao
    return corpo_de_erro(DadosInvalidos.codigo, mensagem, campos)


def _mensagens(valor):
    if isinstance(valor, dict):
        valor = list(valor.values())
    if isinstance(valor, list):
        return [mensagem for item in valor for mensagem in _mensagens(item)]
    return [str(valor)]


def _traducao_fixa(codigo, mensagem):
    def traduzir(_exc):
        return corpo_de_erro(codigo, mensagem)

    return traduzir


def _traduzir_generico(exc):
    codigo = getattr(exc, "default_code", "erro").upper()
    return corpo_de_erro(codigo, MENSAGEM_ERRO_GENERICO)


_NAO_AUTENTICADO = _traducao_fixa("NAO_AUTENTICADO", "Faça login para continuar.")
_SEM_PERMISSAO = _traducao_fixa(
    AcaoNaoPermitida.codigo, AcaoNaoPermitida.mensagem_padrao
)
_NAO_ENCONTRADO = _traducao_fixa(
    RecursoNaoEncontrado.codigo, RecursoNaoEncontrado.mensagem_padrao
)

_TRADUTORES = {
    exceptions.ValidationError: _traduzir_validacao,
    exceptions.ParseError: _traducao_fixa(
        "JSON_INVALIDO", "O corpo da requisição não é um JSON válido."
    ),
    exceptions.NotAuthenticated: _NAO_AUTENTICADO,
    exceptions.AuthenticationFailed: _NAO_AUTENTICADO,
    exceptions.PermissionDenied: _SEM_PERMISSAO,
    PermissaoNegadaDoDjango: _SEM_PERMISSAO,
    exceptions.NotFound: _NAO_ENCONTRADO,
    Http404: _NAO_ENCONTRADO,
    exceptions.MethodNotAllowed: _traducao_fixa(
        "METODO_NAO_PERMITIDO", "Método não permitido para este endereço."
    ),
}
