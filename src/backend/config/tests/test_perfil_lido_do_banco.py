"""O perfil é lido do banco a cada requisição, nunca do token (regra 16).

Fica em config/ porque cruza contas, espacos e reservas.
"""

from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from contas.domain.perfil import PerfilUsuario

pytestmark = pytest.mark.django_db

NOVO_ESPACO = {"nome": "Ginásio Novo", "tipo": "GINASIO", "capacidade": 30}


def _mudar_perfil(usuario, perfil):
    get_user_model().objects.filter(pk=usuario.pk).update(perfil=perfil)


def _cadastrar_espaco(cliente):
    return cliente.post(reverse("espacos:lista"), NOVO_ESPACO, format="json")


def _solicitar(cliente, espaco_id, hora_inicio):
    resposta = cliente.post(
        reverse("reservas:lista"),
        {
            "espaco_id": espaco_id,
            "data": (timezone.localdate() + timedelta(days=1)).isoformat(),
            "hora_inicio": hora_inicio,
            "hora_fim": f"{int(hora_inicio[:2]) + 1:02d}:00",
            "finalidade": "Treino",
        },
        format="json",
    )
    assert resposta.status_code == 201
    return resposta.data["dados"]["id"]


def _confirmar(cliente, reserva_id):
    return cliente.patch(
        reverse("reservas:situacao", args=[reserva_id]),
        {"situacao": "CONFIRMADA"},
        format="json",
    )


def test_gestor_rebaixado_perde_as_permissoes_com_o_mesmo_token(
    cliente_com_token, usuario_gestor, espaco_id
):
    # Arrange
    cliente = cliente_com_token(usuario_gestor)
    propria = _solicitar(cliente, espaco_id, "10:00")
    _mudar_perfil(usuario_gestor, PerfilUsuario.SOLICITANTE)

    # Act
    espaco = _cadastrar_espaco(cliente)
    confirmacao = _confirmar(cliente, propria)

    # Assert
    assert espaco.status_code == 403
    assert espaco.data["erro"]["codigo"] == "ACAO_NAO_PERMITIDA"
    assert confirmacao.status_code == 403
    assert confirmacao.data["erro"]["codigo"] == "ACAO_NAO_PERMITIDA"


def test_gestor_rebaixado_deixa_de_ver_reserva_de_outra_pessoa(
    cliente_com_token, usuario_gestor, usuario_solicitante, espaco_id
):
    # Arrange
    cliente = cliente_com_token(usuario_gestor)
    alheia = _solicitar(cliente_com_token(usuario_solicitante), espaco_id, "10:00")
    _mudar_perfil(usuario_gestor, PerfilUsuario.SOLICITANTE)

    # Act
    resposta = _confirmar(cliente, alheia)

    # Assert
    assert resposta.status_code == 404
    assert resposta.data["erro"]["codigo"] == "RESERVA_NAO_ENCONTRADA"


def test_solicitante_promovido_ganha_as_permissoes_com_o_mesmo_token(
    cliente_com_token, usuario_solicitante, outro_solicitante, espaco_id
):
    # Arrange
    cliente = cliente_com_token(outro_solicitante)
    alheia = _solicitar(cliente_com_token(usuario_solicitante), espaco_id, "10:00")
    assert _cadastrar_espaco(cliente).status_code == 403
    _mudar_perfil(outro_solicitante, PerfilUsuario.GESTOR)

    # Act
    espaco = _cadastrar_espaco(cliente)
    confirmacao = _confirmar(cliente, alheia)

    # Assert
    assert espaco.status_code == 201
    assert confirmacao.status_code == 200
    assert confirmacao.data["dados"]["situacao"] == "CONFIRMADA"
