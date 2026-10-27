from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

URL_RESERVAS = reverse("reservas:lista")
URL_ESPACOS = reverse("espacos:lista")
SENHA = "senha-de-teste-123"
ID_INEXISTENTE = 9999
MOTIVO = "Chuva forte"


def _url_situacao(reserva_id):
    return reverse("reservas:situacao", args=[reserva_id])


def _url_detalhe(reserva_id):
    return reverse("reservas:detalhe", args=[reserva_id])


def _corpo_da_reserva(espaco_id):
    return {
        "espaco_id": espaco_id,
        "data": (timezone.localdate() + timedelta(days=1)).isoformat(),
        "hora_inicio": "10:00",
        "hora_fim": "11:00",
        "finalidade": "Treino",
    }


@pytest.fixture
def cliente():
    usuario = get_user_model().objects.create_user(
        "ana@exemplo.com", SENHA, nome="Ana Souza", matricula="2026001"
    )
    cliente = APIClient()
    cliente.force_authenticate(user=usuario)
    return cliente


@pytest.fixture
def espaco_id(cliente):
    resposta = cliente.post(
        URL_ESPACOS,
        {"nome": "Quadra Coberta", "tipo": "QUADRA_POLIESPORTIVA", "capacidade": 20},
        format="json",
    )
    return resposta.data["dados"]["id"]


@pytest.fixture
def reserva_id(cliente, espaco_id):
    resposta = cliente.post(URL_RESERVAS, _corpo_da_reserva(espaco_id), format="json")
    return resposta.data["dados"]["id"]


def _alterar(cliente, reserva_id, corpo):
    return cliente.patch(_url_situacao(reserva_id), corpo, format="json")


def _detalhe(cliente, reserva_id):
    return cliente.get(_url_detalhe(reserva_id)).data["dados"]


def test_alterar_sem_login_responde_401(reserva_id):
    # Act
    resposta = _alterar(APIClient(), reserva_id, {"situacao": "CONFIRMADA"})

    # Assert
    assert resposta.status_code == 401
    assert resposta.data["erro"]["codigo"] == "NAO_AUTENTICADO"


def test_confirmar_responde_200_com_a_reserva_atualizada(cliente, reserva_id):
    # Act
    resposta = _alterar(cliente, reserva_id, {"situacao": "CONFIRMADA"})

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Reserva confirmada com sucesso."
    assert resposta.data["dados"]["id"] == reserva_id
    assert resposta.data["dados"]["situacao"] == "CONFIRMADA"
    assert resposta.data["dados"]["motivo_da_situacao"] is None


@pytest.mark.parametrize(
    ("caminho", "mensagem"),
    [
        (["CONFIRMADA"], "Reserva confirmada com sucesso."),
        (["RECUSADA"], "Reserva recusada com sucesso."),
        (["CANCELADA"], "Reserva cancelada com sucesso."),
        (["CONFIRMADA", "CONCLUIDA"], "Reserva concluída com sucesso."),
    ],
    ids=["confirmada", "recusada", "cancelada", "concluida"],
)
def test_mensagem_de_sucesso_usa_o_rotulo_da_nova_situacao(
    cliente, reserva_id, caminho, mensagem
):
    # Act
    for situacao in caminho:
        resposta = _alterar(
            cliente, reserva_id, {"situacao": situacao, "motivo": MOTIVO}
        )

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == mensagem


def test_fluxo_da_demonstracao_ate_concluida(cliente, reserva_id):
    # Act
    confirmada = _alterar(cliente, reserva_id, {"situacao": "CONFIRMADA"})
    concluida = _alterar(cliente, reserva_id, {"situacao": "CONCLUIDA"})

    # Assert
    assert confirmada.status_code == 200
    assert concluida.status_code == 200
    detalhe = _detalhe(cliente, reserva_id)
    assert detalhe["situacao"] == "CONCLUIDA"
    assert detalhe["situacao_rotulo"] == "Concluída"


def _acao(situacao, rotulo, exige_motivo=False):
    return {"situacao": situacao, "rotulo": rotulo, "exige_motivo": exige_motivo}


def test_reserva_solicitada_traz_confirmar_recusar_e_cancelar(cliente, reserva_id):
    # Act
    acoes = _detalhe(cliente, reserva_id)["acoes_disponiveis"]

    # Assert
    assert acoes == [
        _acao("CONFIRMADA", "Confirmar"),
        _acao("RECUSADA", "Recusar", exige_motivo=True),
        _acao("CANCELADA", "Cancelar", exige_motivo=True),
    ]


def test_reserva_confirmada_traz_cancelar_e_concluir(cliente, reserva_id):
    # Act
    resposta = _alterar(cliente, reserva_id, {"situacao": "CONFIRMADA"})

    # Assert
    assert resposta.data["dados"]["acoes_disponiveis"] == [
        _acao("CANCELADA", "Cancelar", exige_motivo=True),
        _acao("CONCLUIDA", "Concluir"),
    ]


def test_reserva_concluida_nao_traz_acoes(cliente, reserva_id):
    # Arrange
    _alterar(cliente, reserva_id, {"situacao": "CONFIRMADA"})

    # Act
    resposta = _alterar(cliente, reserva_id, {"situacao": "CONCLUIDA"})

    # Assert
    assert resposta.data["dados"]["acoes_disponiveis"] == []
    assert _detalhe(cliente, reserva_id)["acoes_disponiveis"] == []


def test_transicao_proibida_responde_409_e_preserva_a_reserva(cliente, reserva_id):
    # Arrange
    antes = _detalhe(cliente, reserva_id)

    # Act
    resposta = _alterar(cliente, reserva_id, {"situacao": "CONCLUIDA"})

    # Assert
    assert resposta.status_code == 409
    assert resposta.data == {
        "erro": {
            "codigo": "TRANSICAO_DE_SITUACAO_INVALIDA",
            "mensagem": "Não é possível alterar uma reserva Solicitada para Concluída.",
        }
    }
    assert _detalhe(cliente, reserva_id) == antes


def test_reserva_concluida_nao_pode_ser_cancelada(cliente, reserva_id):
    # Arrange
    _alterar(cliente, reserva_id, {"situacao": "CONFIRMADA"})
    _alterar(cliente, reserva_id, {"situacao": "CONCLUIDA"})

    # Act
    resposta = _alterar(
        cliente, reserva_id, {"situacao": "CANCELADA", "motivo": MOTIVO}
    )

    # Assert
    assert resposta.status_code == 409
    assert resposta.data["erro"]["codigo"] == "TRANSICAO_DE_SITUACAO_INVALIDA"
    assert _detalhe(cliente, reserva_id)["situacao"] == "CONCLUIDA"


def test_recusar_sem_motivo_responde_400_no_campo_motivo(cliente, reserva_id):
    # Act
    resposta = _alterar(cliente, reserva_id, {"situacao": "RECUSADA"})

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "MOTIVO_OBRIGATORIO"
    assert "motivo" in resposta.data["erro"]["campos"]
    assert _detalhe(cliente, reserva_id)["situacao"] == "SOLICITADA"


@pytest.mark.parametrize(
    ("corpo", "codigo"),
    [
        ({}, "DADOS_INVALIDOS"),
        ({"situacao": ""}, "DADOS_INVALIDOS"),
        ({"situacao": "PENDENTE"}, "SITUACAO_INVALIDA"),
    ],
    ids=["sem-situacao", "situacao-vazia", "situacao-desconhecida"],
)
def test_situacao_ausente_ou_invalida_responde_400(cliente, reserva_id, corpo, codigo):
    # Act
    resposta = _alterar(cliente, reserva_id, corpo)

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == codigo
    assert "situacao" in resposta.data["erro"]["campos"]


def test_reserva_inexistente_responde_404(cliente):
    # Act
    resposta = _alterar(cliente, ID_INEXISTENTE, {"situacao": "CONFIRMADA"})

    # Assert
    assert resposta.status_code == 404
    assert resposta.data["erro"]["codigo"] == "RESERVA_NAO_ENCONTRADA"


@pytest.mark.parametrize("metodo", ["put", "post"])
def test_outros_metodos_respondem_405(cliente, reserva_id, metodo):
    # Act
    resposta = getattr(cliente, metodo)(
        _url_situacao(reserva_id), {"situacao": "CONFIRMADA"}, format="json"
    )

    # Assert
    assert resposta.status_code == 405
    assert resposta.data["erro"]["codigo"] == "METODO_NAO_PERMITIDO"


def test_cancelar_libera_o_horario_para_nova_reserva(cliente, espaco_id, reserva_id):
    # Arrange
    _alterar(cliente, reserva_id, {"situacao": "CANCELADA", "motivo": MOTIVO})

    # Act
    resposta = cliente.post(URL_RESERVAS, _corpo_da_reserva(espaco_id), format="json")

    # Assert
    assert resposta.status_code == 201
    assert resposta.data["dados"]["id"] != reserva_id
