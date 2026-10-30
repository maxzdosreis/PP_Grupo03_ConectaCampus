import json
from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from reservas.domain.excecoes import DataRetroativa

pytestmark = pytest.mark.django_db

URL_OCUPACAO = reverse("reservas:ocupacao")
URL_RESERVAS = reverse("reservas:lista")
FINALIDADE = "Treino secreto do time de vôlei"
MOTIVO = "Mudança de planos do time"
ID_INEXISTENTE = 9999


def _amanha():
    return timezone.localdate() + timedelta(days=1)


def _consultar(cliente, espaco_id, data):
    return cliente.get(URL_OCUPACAO, {"espaco": espaco_id, "data": data.isoformat()})


def _solicitar(cliente, espaco_id, hora_inicio, hora_fim):
    resposta = cliente.post(
        URL_RESERVAS,
        {
            "espaco_id": espaco_id,
            "data": _amanha().isoformat(),
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim,
            "finalidade": FINALIDADE,
        },
        format="json",
    )
    assert resposta.status_code == 201
    return resposta.data["dados"]["id"]


@pytest.fixture
def cliente_do_outro(outro_solicitante):
    cliente = APIClient()
    cliente.force_authenticate(user=outro_solicitante)
    return cliente


def test_sem_login_responde_401(espaco_id):
    # Act
    resposta = _consultar(APIClient(), espaco_id, _amanha())

    # Assert
    assert resposta.status_code == 401
    assert resposta.data["erro"]["codigo"] == "NAO_AUTENTICADO"


@pytest.mark.parametrize("ausente", ["espaco", "data"])
def test_sem_espaco_ou_sem_data_responde_400_com_o_campo(
    cliente_solicitante, espaco_id, ausente
):
    # Arrange
    parametros = {"espaco": espaco_id, "data": _amanha().isoformat()}
    del parametros[ausente]

    # Act
    resposta = cliente_solicitante.get(URL_OCUPACAO, parametros)

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "DADOS_INVALIDOS"
    assert list(resposta.data["erro"]["campos"]) == [ausente]


def test_dia_livre_responde_com_o_funcionamento_inteiro(cliente_solicitante, espaco_id):
    # Act
    resposta = _consultar(cliente_solicitante, espaco_id, _amanha())

    # Assert
    assert resposta.status_code == 200
    assert resposta.data == {
        "mensagem": "Nenhum horário ocupado neste dia.",
        "dados": {
            "data": _amanha().isoformat(),
            "horario_de_abertura": "07:00",
            "horario_de_fechamento": "22:00",
            "reservavel": True,
            "motivo_indisponivel": None,
            "ocupados": [],
            "livres": [{"hora_inicio": "07:00", "hora_fim": "22:00"}],
        },
    }


def test_solicitante_ve_a_reserva_de_outra_pessoa_sem_nenhum_dado_pessoal(
    cliente_solicitante,
    cliente_gestor,
    cliente_do_outro,
    outro_solicitante,
    espaco_id,
):
    # Arrange
    reserva_id = _solicitar(cliente_do_outro, espaco_id, "10:00", "11:00")
    cancelada_id = _solicitar(cliente_do_outro, espaco_id, "15:00", "16:00")
    cliente_gestor.patch(
        reverse("reservas:situacao", args=[cancelada_id]),
        {"situacao": "CANCELADA", "motivo": MOTIVO},
        format="json",
    )
    _solicitar(cliente_do_outro, espaco_id, "18:00", "19:00")
    cliente_gestor.patch(
        reverse("reservas:situacao", args=[reserva_id]),
        {"situacao": "CONFIRMADA"},
        format="json",
    )

    # Act
    resposta = _consultar(cliente_solicitante, espaco_id, _amanha())

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "2 horários ocupados neste dia."
    dados = resposta.data["dados"]
    assert dados["ocupados"] == [
        {
            "hora_inicio": "10:00",
            "hora_fim": "11:00",
            "situacao": "CONFIRMADA",
            "situacao_rotulo": "Confirmada",
        },
        {
            "hora_inicio": "18:00",
            "hora_fim": "19:00",
            "situacao": "SOLICITADA",
            "situacao_rotulo": "Solicitada",
        },
    ]
    corpo = json.dumps(resposta.data, ensure_ascii=False)
    for proibido in (
        outro_solicitante.nome,
        outro_solicitante.matricula,
        outro_solicitante.email,
        FINALIDADE,
        MOTIVO,
        '"id"',
        "usuario_id",
        "solicitante",
        "finalidade",
        "motivo_da_situacao",
    ):
        assert proibido not in corpo, proibido


def test_livres_sao_coerentes_com_os_ocupados(cliente_solicitante, espaco_id):
    # Arrange
    _solicitar(cliente_solicitante, espaco_id, "10:00", "11:00")
    _solicitar(cliente_solicitante, espaco_id, "11:20", "12:00")

    # Act
    resposta = _consultar(cliente_solicitante, espaco_id, _amanha())

    # Assert
    assert resposta.data["dados"]["livres"] == [
        {"hora_inicio": "07:00", "hora_fim": "10:00"},
        {"hora_inicio": "12:00", "hora_fim": "22:00"},
    ]


def test_um_horario_ocupado_usa_a_mensagem_no_singular(cliente_solicitante, espaco_id):
    # Arrange
    _solicitar(cliente_solicitante, espaco_id, "10:00", "11:00")

    # Act
    resposta = _consultar(cliente_solicitante, espaco_id, _amanha())

    # Assert
    assert resposta.data["mensagem"] == "1 horário ocupado neste dia."


def test_ontem_nao_e_reservavel_e_traz_a_mensagem_do_dominio(
    cliente_solicitante, espaco_id
):
    # Act
    resposta = _consultar(
        cliente_solicitante, espaco_id, timezone.localdate() - timedelta(days=1)
    )

    # Assert
    assert resposta.status_code == 200
    dados = resposta.data["dados"]
    assert dados["reservavel"] is False
    assert dados["motivo_indisponivel"] == DataRetroativa().mensagem
    assert dados["livres"] == []


def test_espaco_inexistente_responde_404(cliente_solicitante):
    # Act
    resposta = _consultar(cliente_solicitante, ID_INEXISTENTE, _amanha())

    # Assert
    assert resposta.status_code == 404
    assert resposta.data["erro"]["codigo"] == "ESPACO_NAO_ENCONTRADO"


def test_espaco_inativo_responde_409(cliente_solicitante, cliente_gestor, espaco_id):
    # Arrange
    cliente_gestor.post(reverse("espacos:desativar", args=[espaco_id]))

    # Act
    resposta = _consultar(cliente_solicitante, espaco_id, _amanha())

    # Assert
    assert resposta.status_code == 409
    assert resposta.data["erro"]["codigo"] == "ESPACO_INATIVO"
