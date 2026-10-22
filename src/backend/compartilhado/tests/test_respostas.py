import pytest

from compartilhado.api.respostas import (
    corpo_de_erro,
    mensagem_de_contagem,
    resposta_sucesso,
)


def test_resposta_sucesso_devolve_mensagem_dados_e_status_pedidos():
    # Act
    resposta = resposta_sucesso("Espaço cadastrado com sucesso.", {"id": 1}, 201)

    # Assert
    assert resposta.status_code == 201
    assert resposta.data == {
        "mensagem": "Espaço cadastrado com sucesso.",
        "dados": {"id": 1},
    }


def test_resposta_sucesso_sem_dados_usa_status_200_e_dados_nulos():
    # Act
    resposta = resposta_sucesso("Tudo certo.")

    # Assert
    assert resposta.status_code == 200
    assert resposta.data == {"mensagem": "Tudo certo.", "dados": None}


def test_corpo_de_erro_sem_campos_nao_inclui_a_chave_campos():
    # Act
    corpo = corpo_de_erro("CONFLITO_DE_HORARIO", "Horário ocupado.")

    # Assert
    assert corpo == {
        "erro": {"codigo": "CONFLITO_DE_HORARIO", "mensagem": "Horário ocupado."}
    }


def test_corpo_de_erro_com_campos_inclui_os_campos():
    # Act
    corpo = corpo_de_erro("DADOS_INVALIDOS", "Verifique.", {"nome": ["Obrigatório."]})

    # Assert
    assert corpo["erro"]["campos"] == {"nome": ["Obrigatório."]}


@pytest.mark.parametrize(
    ("total", "esperada"),
    [
        (0, "Nenhum item encontrado."),
        (1, "1 item encontrado."),
        (3, "3 itens encontrados."),
    ],
    ids=["nenhum", "um", "varios"],
)
def test_mensagem_de_contagem_escolhe_o_texto_pelo_total(total, esperada):
    # Act
    mensagem = mensagem_de_contagem(
        total,
        nenhum="Nenhum item encontrado.",
        um="1 item encontrado.",
        varios="{total} itens encontrados.",
    )

    # Assert
    assert mensagem == esperada
