import pytest

from compartilhado.domain.erros import (
    AcaoNaoPermitida,
    CampoObrigatorioAusente,
    ConflitoDeEstado,
    DadosInvalidos,
    RecursoNaoEncontrado,
    TextoMuitoLongo,
)


@pytest.mark.parametrize(
    ("categoria", "codigo", "mensagem"),
    [
        (DadosInvalidos, "DADOS_INVALIDOS", "Verifique os dados informados."),
        (
            RecursoNaoEncontrado,
            "NAO_ENCONTRADO",
            "O recurso solicitado não foi encontrado.",
        ),
        (
            ConflitoDeEstado,
            "CONFLITO_DE_ESTADO",
            "A operação não é compatível com a situação atual.",
        ),
        (
            AcaoNaoPermitida,
            "ACAO_NAO_PERMITIDA",
            "Você não tem permissão para realizar esta ação.",
        ),
    ],
)
def test_categoria_sem_mensagem_usa_codigo_e_mensagem_padrao(
    categoria, codigo, mensagem
):
    # Act
    erro = categoria()

    # Assert
    assert erro.codigo == codigo
    assert erro.mensagem == mensagem
    assert str(erro) == mensagem
    assert erro.campo is None


def test_mensagem_personalizada_substitui_a_padrao():
    # Act
    erro = ConflitoDeEstado("A reserva já foi concluída.")

    # Assert
    assert erro.mensagem == "A reserva já foi concluída."
    assert str(erro) == "A reserva já foi concluída."
    assert erro.codigo == "CONFLITO_DE_ESTADO"


def test_campo_obrigatorio_ausente_informa_rotulo_e_campo():
    # Act
    erro = CampoObrigatorioAusente("hora_inicio", "Hora de início")

    # Assert
    assert isinstance(erro, DadosInvalidos)
    assert erro.codigo == "CAMPO_OBRIGATORIO_AUSENTE"
    assert erro.campo == "hora_inicio"
    assert str(erro) == 'O campo "Hora de início" é obrigatório.'


def test_texto_muito_longo_informa_rotulo_limite_e_campo():
    # Act
    erro = TextoMuitoLongo("finalidade", "Finalidade", 200)

    # Assert
    assert isinstance(erro, DadosInvalidos)
    assert erro.codigo == "TEXTO_MUITO_LONGO"
    assert erro.campo == "finalidade"
    assert erro.limite == 200
    assert str(erro) == 'O campo "Finalidade" deve ter no máximo 200 caracteres.'
