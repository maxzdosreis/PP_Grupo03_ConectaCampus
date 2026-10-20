from compartilhado.api.respostas import corpo_de_erro, resposta_sucesso


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
