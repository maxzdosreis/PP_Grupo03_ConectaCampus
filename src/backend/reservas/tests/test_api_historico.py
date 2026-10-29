from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from reservas.tests.historico import verificar_historico_coerente

pytestmark = pytest.mark.django_db

URL_RESERVAS = reverse("reservas:lista")
ID_INEXISTENTE = 9999
MOTIVO = "Chuva forte"


def _url_historico(reserva_id):
    return reverse("reservas:historico", args=[reserva_id])


def _url_situacao(reserva_id):
    return reverse("reservas:situacao", args=[reserva_id])


@pytest.fixture
def reserva_id(cliente_solicitante, espaco_id):
    resposta = cliente_solicitante.post(
        URL_RESERVAS,
        {
            "espaco_id": espaco_id,
            "data": (timezone.localdate() + timedelta(days=1)).isoformat(),
            "hora_inicio": "10:00",
            "hora_fim": "11:00",
            "finalidade": "Treino",
        },
        format="json",
    )
    return resposta.data["dados"]["id"]


def _alterar(cliente, reserva_id, corpo):
    return cliente.patch(_url_situacao(reserva_id), corpo, format="json")


def _historico(cliente, reserva_id):
    return cliente.get(_url_historico(reserva_id))


def test_fluxo_completo_aparece_no_historico_em_ordem(
    cliente_solicitante, cliente_gestor, reserva_id
):
    # Arrange
    _alterar(cliente_gestor, reserva_id, {"situacao": "CONFIRMADA"})
    _alterar(cliente_gestor, reserva_id, {"situacao": "CONCLUIDA"})

    # Act
    resposta = _historico(cliente_gestor, reserva_id)

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Histórico da reserva."
    registros = resposta.data["dados"]
    verificar_historico_coerente(registros, "CONCLUIDA")
    assert [
        (r["situacao_anterior_rotulo"], r["situacao_nova_rotulo"]) for r in registros
    ] == [
        (None, "Solicitada"),
        ("Solicitada", "Confirmada"),
        ("Confirmada", "Concluída"),
    ]
    assert [r["autor"] for r in registros] == [
        {"nome": "Ana Souza"},
        {"nome": "Gestora de Teste"},
        {"nome": "Gestora de Teste"},
    ]
    assert [r["motivo"] for r in registros] == [None, None, None]


def test_registrado_em_sai_em_iso_8601_no_fuso_de_sao_paulo(
    cliente_solicitante, reserva_id
):
    # Act
    (registro,) = _historico(cliente_solicitante, reserva_id).data["dados"]

    # Assert
    registrado_em = datetime.fromisoformat(registro["registrado_em"])
    assert registro["registrado_em"].endswith("-03:00")
    assert abs(timezone.now() - registrado_em) < timedelta(minutes=1)


def test_registro_nao_expoe_o_id_do_autor(cliente_gestor, reserva_id):
    # Act
    (registro,) = _historico(cliente_gestor, reserva_id).data["dados"]

    # Assert
    assert set(registro) == {
        "situacao_anterior",
        "situacao_anterior_rotulo",
        "situacao_nova",
        "situacao_nova_rotulo",
        "motivo",
        "autor",
        "registrado_em",
    }
    assert registro["autor"] == {"nome": "Ana Souza"}


def test_cancelamento_aparece_com_o_motivo(cliente_solicitante, reserva_id):
    # Arrange
    _alterar(
        cliente_solicitante, reserva_id, {"situacao": "CANCELADA", "motivo": MOTIVO}
    )

    # Act
    registros = _historico(cliente_solicitante, reserva_id).data["dados"]

    # Assert
    assert registros[-1]["situacao_anterior"] == "SOLICITADA"
    assert registros[-1]["situacao_nova"] == "CANCELADA"
    assert registros[-1]["motivo"] == MOTIVO
    assert registros[-1]["autor"] == {"nome": "Ana Souza"}


def test_tentativa_recusada_nao_aparece_no_historico(cliente_solicitante, reserva_id):
    # Arrange
    recusada = _alterar(cliente_solicitante, reserva_id, {"situacao": "CONFIRMADA"})

    # Act
    registros = _historico(cliente_solicitante, reserva_id).data["dados"]

    # Assert
    assert recusada.status_code == 403
    assert [r["situacao_nova"] for r in registros] == ["SOLICITADA"]


def test_solicitante_pedindo_historico_de_outra_pessoa_recebe_404(
    outro_solicitante, reserva_id
):
    # Arrange
    cliente = APIClient()
    cliente.force_authenticate(user=outro_solicitante)

    # Act
    resposta = _historico(cliente, reserva_id)

    # Assert
    assert resposta.status_code == 404
    assert resposta.data["erro"]["codigo"] == "RESERVA_NAO_ENCONTRADA"


def test_historico_de_reserva_inexistente_responde_404(cliente_gestor):
    # Act
    resposta = _historico(cliente_gestor, ID_INEXISTENTE)

    # Assert
    assert resposta.status_code == 404
    assert resposta.data["erro"]["codigo"] == "RESERVA_NAO_ENCONTRADA"


def test_historico_sem_login_responde_401(reserva_id):
    # Act
    resposta = _historico(APIClient(), reserva_id)

    # Assert
    assert resposta.status_code == 401
    assert resposta.data["erro"]["codigo"] == "NAO_AUTENTICADO"


@pytest.mark.parametrize("metodo", ["post", "put", "patch", "delete"])
def test_historico_nao_aceita_alteracao_nem_exclusao(
    cliente_gestor, reserva_id, metodo
):
    # Act
    resposta = getattr(cliente_gestor, metodo)(_url_historico(reserva_id))

    # Assert
    assert resposta.status_code == 405
    assert resposta.data["erro"]["codigo"] == "METODO_NAO_PERMITIDO"
