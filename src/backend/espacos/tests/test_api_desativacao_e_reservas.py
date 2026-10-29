from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

pytestmark = pytest.mark.django_db

URL_RESERVAS = reverse("reservas:lista")


def _solicitar(cliente, espaco_id, hora_inicio, hora_fim):
    amanha = timezone.localdate() + timedelta(days=1)
    return cliente.post(
        URL_RESERVAS,
        {
            "espaco_id": espaco_id,
            "data": amanha.isoformat(),
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim,
            "finalidade": "Treino",
        },
        format="json",
    )


def _situacoes_das_acoes(reserva):
    return [acao["situacao"] for acao in reserva["acoes_disponiveis"]]


def test_espaco_desativado_recusa_nova_reserva_com_409(
    cliente_gestor, cliente_solicitante, espaco_id
):
    # Arrange
    cliente_gestor.post(reverse("espacos:desativar", args=[espaco_id]))

    # Act
    resposta = _solicitar(cliente_solicitante, espaco_id, "10:00", "11:00")

    # Assert
    assert resposta.status_code == 409
    assert resposta.data["erro"] == {
        "codigo": "ESPACO_INATIVO",
        "mensagem": "Este espaço está inativo e não aceita reservas.",
    }


def test_reserva_existente_continua_valendo_depois_de_desativar(
    cliente_gestor, cliente_solicitante, espaco_id
):
    # Arrange
    reserva_id = _solicitar(cliente_solicitante, espaco_id, "10:00", "11:00").data[
        "dados"
    ]["id"]

    # Act
    cliente_gestor.post(reverse("espacos:desativar", args=[espaco_id]))

    # Assert
    reservas = cliente_gestor.get(URL_RESERVAS, {"espaco": espaco_id}).data["dados"]
    assert [reserva["id"] for reserva in reservas] == [reserva_id]
    assert _situacoes_das_acoes(reservas[0]) == ["CONFIRMADA", "RECUSADA", "CANCELADA"]
    confirmacao = cliente_gestor.patch(
        reverse("reservas:situacao", args=[reserva_id]),
        {"situacao": "CONFIRMADA"},
        format="json",
    )
    assert confirmacao.status_code == 200


def test_reativar_volta_a_aceitar_reservas(
    cliente_gestor, cliente_solicitante, espaco_id
):
    # Arrange
    cliente_gestor.post(reverse("espacos:desativar", args=[espaco_id]))
    cliente_gestor.post(reverse("espacos:ativar", args=[espaco_id]))

    # Act
    resposta = _solicitar(cliente_solicitante, espaco_id, "14:00", "15:00")

    # Assert
    assert resposta.status_code == 201
    assert resposta.data["dados"]["situacao"] == "SOLICITADA"
