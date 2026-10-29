import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

URL_LISTA = reverse("espacos:lista")
ID_INEXISTENTE = 9999


def _url(nome_da_rota, espaco_id):
    return reverse(f"espacos:{nome_da_rota}", args=[espaco_id])


def _editar(cliente, espaco_id, corpo):
    return cliente.patch(_url("detalhe", espaco_id), corpo, format="json")


def _desativar(cliente, espaco_id):
    return cliente.post(_url("desativar", espaco_id))


def _ativar(cliente, espaco_id):
    return cliente.post(_url("ativar", espaco_id))


def _espaco_na_listagem(cliente, espaco_id):
    espacos = cliente.get(URL_LISTA).data["dados"]
    return next(espaco for espaco in espacos if espaco["id"] == espaco_id)


def test_editar_responde_200_e_a_listagem_mostra_os_dados_novos(
    cliente_gestor, espaco_id
):
    # Act
    resposta = _editar(
        cliente_gestor,
        espaco_id,
        {"nome": "  Quadra   Reformada ", "tipo": "GINASIO", "capacidade": "45"},
    )

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Espaço atualizado com sucesso."
    esperado = {
        "id": espaco_id,
        "nome": "Quadra Reformada",
        "tipo": "GINASIO",
        "tipo_rotulo": "Ginásio",
        "capacidade": 45,
        "ativo": True,
    }
    assert resposta.data["dados"] == esperado
    assert _espaco_na_listagem(cliente_gestor, espaco_id) == esperado


def test_editar_so_a_capacidade_mantem_os_outros_campos(cliente_gestor, espaco_id):
    # Act
    resposta = _editar(cliente_gestor, espaco_id, {"capacidade": 12})

    # Assert
    assert resposta.status_code == 200
    dados = resposta.data["dados"]
    assert (dados["nome"], dados["tipo"], dados["capacidade"]) == (
        "Quadra Coberta",
        "QUADRA_POLIESPORTIVA",
        12,
    )


@pytest.mark.parametrize(
    ("corpo", "status", "codigo", "campo"),
    [
        ({"capacidade": 0}, 400, "CAPACIDADE_INVALIDA", "capacidade"),
        ({"capacidade": "abc"}, 400, "DADOS_INVALIDOS", "capacidade"),
        ({"nome": "  "}, 400, "CAMPO_OBRIGATORIO_AUSENTE", "nome"),
        ({"tipo": "PISCINA"}, 400, "TIPO_DE_ESPACO_INVALIDO", "tipo"),
        ({"nome": "ginásio a"}, 409, "NOME_DE_ESPACO_JA_CADASTRADO", "nome"),
    ],
    ids=[
        "capacidade-zero",
        "capacidade-texto",
        "nome-vazio",
        "tipo-desconhecido",
        "nome-de-outro-espaco",
    ],
)
def test_editar_com_dado_invalido_responde_erro_no_campo_e_nao_grava(
    cliente_gestor, espaco_id, corpo, status, codigo, campo
):
    # Arrange
    cliente_gestor.post(
        URL_LISTA,
        {"nome": "Ginásio A", "tipo": "GINASIO", "capacidade": 50},
        format="json",
    )
    antes = _espaco_na_listagem(cliente_gestor, espaco_id)

    # Act
    resposta = _editar(cliente_gestor, espaco_id, corpo)

    # Assert
    assert resposta.status_code == status
    assert resposta.data["erro"]["codigo"] == codigo
    assert campo in resposta.data["erro"]["campos"]
    assert _espaco_na_listagem(cliente_gestor, espaco_id) == antes


def test_editar_sem_nenhum_campo_responde_400(cliente_gestor, espaco_id):
    # Act
    resposta = _editar(cliente_gestor, espaco_id, {})

    # Assert
    assert resposta.status_code == 400
    assert resposta.data == {
        "erro": {
            "codigo": "NENHUMA_ALTERACAO_INFORMADA",
            "mensagem": "Informe ao menos um campo para alterar.",
        }
    }


def test_ativo_no_corpo_do_patch_e_ignorado(cliente_gestor, espaco_id):
    # Act
    resposta = _editar(cliente_gestor, espaco_id, {"capacidade": 30, "ativo": False})

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"]["ativo"] is True
    assert _espaco_na_listagem(cliente_gestor, espaco_id)["ativo"] is True


def test_so_ativo_no_corpo_do_patch_conta_como_nenhuma_alteracao(
    cliente_gestor, espaco_id
):
    # Act
    resposta = _editar(cliente_gestor, espaco_id, {"ativo": False})

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "NENHUMA_ALTERACAO_INFORMADA"
    assert _espaco_na_listagem(cliente_gestor, espaco_id)["ativo"] is True


@pytest.mark.parametrize(
    "agir",
    [
        lambda cliente: _editar(cliente, ID_INEXISTENTE, {"capacidade": 10}),
        lambda cliente: _desativar(cliente, ID_INEXISTENTE),
        lambda cliente: _ativar(cliente, ID_INEXISTENTE),
    ],
    ids=["editar", "desativar", "ativar"],
)
def test_acoes_em_espaco_inexistente_respondem_404(cliente_gestor, agir):
    # Act
    resposta = agir(cliente_gestor)

    # Assert
    assert resposta.status_code == 404
    assert resposta.data["erro"]["codigo"] == "ESPACO_NAO_ENCONTRADO"


def test_desativar_responde_200_e_de_novo_responde_409(cliente_gestor, espaco_id):
    # Act
    primeira = _desativar(cliente_gestor, espaco_id)
    segunda = _desativar(cliente_gestor, espaco_id)

    # Assert
    assert primeira.status_code == 200
    assert primeira.data["mensagem"] == (
        "Espaço desativado. Novas reservas ficam bloqueadas; "
        "as existentes continuam valendo."
    )
    assert primeira.data["dados"]["ativo"] is False
    assert segunda.status_code == 409
    assert segunda.data == {
        "erro": {
            "codigo": "ESPACO_JA_INATIVO",
            "mensagem": "Este espaço já está inativo.",
        }
    }
    assert _espaco_na_listagem(cliente_gestor, espaco_id)["ativo"] is False


def test_ativar_espaco_inativo_responde_200_e_de_novo_responde_409(
    cliente_gestor, espaco_id
):
    # Arrange
    _desativar(cliente_gestor, espaco_id)

    # Act
    primeira = _ativar(cliente_gestor, espaco_id)
    segunda = _ativar(cliente_gestor, espaco_id)

    # Assert
    assert primeira.status_code == 200
    assert primeira.data["mensagem"] == "Espaço reativado."
    assert primeira.data["dados"]["ativo"] is True
    assert segunda.status_code == 409
    assert segunda.data["erro"]["codigo"] == "ESPACO_JA_ATIVO"


@pytest.mark.parametrize(
    "agir",
    [
        lambda cliente, espaco_id: _editar(cliente, espaco_id, {"capacidade": 99}),
        _desativar,
        _ativar,
    ],
    ids=["editar", "desativar", "ativar"],
)
def test_solicitante_nao_edita_desativa_nem_ativa_e_nada_muda(
    cliente_solicitante, cliente_gestor, espaco_id, agir
):
    # Arrange
    antes = _espaco_na_listagem(cliente_gestor, espaco_id)

    # Act
    resposta = agir(cliente_solicitante, espaco_id)

    # Assert
    assert resposta.status_code == 403
    assert resposta.data["erro"]["codigo"] == "ACAO_NAO_PERMITIDA"
    assert _espaco_na_listagem(cliente_gestor, espaco_id) == antes
