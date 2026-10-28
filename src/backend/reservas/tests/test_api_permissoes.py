from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

URL_RESERVAS = reverse("reservas:lista")
MOTIVO = "Não poderei comparecer"


def _url_detalhe(reserva_id):
    return reverse("reservas:detalhe", args=[reserva_id])


def _url_situacao(reserva_id):
    return reverse("reservas:situacao", args=[reserva_id])


def _solicitar(cliente, espaco_id, hora_inicio, hora_fim):
    resposta = cliente.post(
        URL_RESERVAS,
        {
            "espaco_id": espaco_id,
            "data": (timezone.localdate() + timedelta(days=1)).isoformat(),
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim,
            "finalidade": "Treino",
        },
        format="json",
    )
    assert resposta.status_code == 201
    return resposta.data["dados"]["id"]


def _alterar(cliente, reserva_id, corpo):
    return cliente.patch(_url_situacao(reserva_id), corpo, format="json")


def _ids_de(resposta):
    return [reserva["id"] for reserva in resposta.data["dados"]]


def _rotulos_das_acoes(reserva):
    return [acao["rotulo"] for acao in reserva["acoes_disponiveis"]]


@pytest.fixture
def cliente_do_outro(outro_solicitante):
    cliente = APIClient()
    cliente.force_authenticate(user=outro_solicitante)
    return cliente


@pytest.fixture
def reservas(cliente_solicitante, cliente_do_outro, espaco_id):
    return {
        "propria": _solicitar(cliente_solicitante, espaco_id, "10:00", "11:00"),
        "alheia": _solicitar(cliente_do_outro, espaco_id, "14:00", "15:00"),
    }


@pytest.mark.parametrize(
    "url",
    [reverse("reservas:situacoes"), reverse("espacos:tipos"), reverse("health")],
    ids=["situacoes", "tipos", "health"],
)
def test_vocabularios_e_health_nao_exigem_login(url):
    # Act
    resposta = APIClient().get(url)

    # Assert
    assert resposta.status_code == 200


@pytest.mark.parametrize(
    "parametros",
    [
        {},
        {"minhas": "false"},
        {"solicitante": "bruno"},
        {"solicitante": "2026002"},
    ],
    ids=["sem-filtros", "minhas-false", "nome-do-outro", "matricula-do-outro"],
)
def test_solicitante_so_lista_as_proprias(cliente_solicitante, reservas, parametros):
    # Act
    resposta = cliente_solicitante.get(URL_RESERVAS, parametros)

    # Assert
    assert resposta.status_code == 200
    assert reservas["alheia"] not in _ids_de(resposta)
    assert all(
        reserva["solicitante"]["matricula"] == "2026001"
        for reserva in resposta.data["dados"]
    )


def test_solicitante_sem_filtros_ve_a_propria(cliente_solicitante, reservas):
    # Act
    resposta = cliente_solicitante.get(URL_RESERVAS)

    # Assert
    assert _ids_de(resposta) == [reservas["propria"]]
    assert resposta.data["mensagem"] == "1 reserva encontrada."


def test_gestor_lista_todas_e_filtra_por_solicitante(cliente_gestor, reservas):
    # Act
    todas = cliente_gestor.get(URL_RESERVAS)
    do_outro = cliente_gestor.get(URL_RESERVAS, {"solicitante": "bruno"})

    # Assert
    assert _ids_de(todas) == [reservas["propria"], reservas["alheia"]]
    assert _ids_de(do_outro) == [reservas["alheia"]]


def test_detalhe_de_outra_pessoa_para_o_solicitante_responde_404(
    cliente_solicitante, reservas
):
    # Act
    resposta = cliente_solicitante.get(_url_detalhe(reservas["alheia"]))

    # Assert
    assert resposta.status_code == 404
    assert resposta.data == {
        "erro": {
            "codigo": "RESERVA_NAO_ENCONTRADA",
            "mensagem": f"Reserva de código {reservas['alheia']} não encontrada.",
        }
    }


def test_gestor_ve_o_detalhe_de_qualquer_reserva(cliente_gestor, reservas):
    # Act
    resposta = cliente_gestor.get(_url_detalhe(reservas["alheia"]))

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"]["id"] == reservas["alheia"]


def test_solicitante_confirmando_a_propria_responde_403_sem_mudar_nada(
    cliente_solicitante, reservas
):
    # Arrange
    antes = cliente_solicitante.get(_url_detalhe(reservas["propria"])).data["dados"]

    # Act
    resposta = _alterar(
        cliente_solicitante, reservas["propria"], {"situacao": "CONFIRMADA"}
    )

    # Assert
    assert resposta.status_code == 403
    assert resposta.data == {
        "erro": {
            "codigo": "ACAO_NAO_PERMITIDA",
            "mensagem": "Somente o gestor pode confirmar reservas.",
        }
    }
    depois = cliente_solicitante.get(_url_detalhe(reservas["propria"])).data["dados"]
    assert depois == antes


def test_solicitante_cancela_a_propria(cliente_solicitante, reservas):
    # Act
    resposta = _alterar(
        cliente_solicitante,
        reservas["propria"],
        {"situacao": "CANCELADA", "motivo": MOTIVO},
    )

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"]["situacao"] == "CANCELADA"
    assert resposta.data["dados"]["motivo_da_situacao"] == MOTIVO


def test_solicitante_cancelando_a_de_outra_pessoa_responde_404_sem_mudar_nada(
    cliente_solicitante, cliente_gestor, reservas
):
    # Act
    resposta = _alterar(
        cliente_solicitante,
        reservas["alheia"],
        {"situacao": "CANCELADA", "motivo": MOTIVO},
    )

    # Assert
    assert resposta.status_code == 404
    assert resposta.data["erro"]["codigo"] == "RESERVA_NAO_ENCONTRADA"
    alheia = cliente_gestor.get(_url_detalhe(reservas["alheia"])).data["dados"]
    assert alheia["situacao"] == "SOLICITADA"


def test_gestor_confirma(cliente_gestor, reservas):
    # Act
    resposta = _alterar(cliente_gestor, reservas["propria"], {"situacao": "CONFIRMADA"})

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Reserva confirmada com sucesso."


def test_acoes_do_solicitante_na_propria_solicitada_sao_so_cancelar(
    cliente_solicitante, reservas
):
    # Act
    reserva = cliente_solicitante.get(_url_detalhe(reservas["propria"])).data["dados"]

    # Assert
    assert reserva["acoes_disponiveis"] == [
        {"situacao": "CANCELADA", "rotulo": "Cancelar", "exige_motivo": True}
    ]


def test_acoes_do_gestor_na_solicitada_sao_confirmar_recusar_e_cancelar(
    cliente_gestor, reservas
):
    # Act
    reserva = cliente_gestor.get(_url_detalhe(reservas["propria"])).data["dados"]

    # Assert
    assert _rotulos_das_acoes(reserva) == ["Confirmar", "Recusar", "Cancelar"]


def test_solicitante_numa_concluida_nao_tem_acoes(
    cliente_solicitante, cliente_gestor, reservas
):
    # Arrange
    _alterar(cliente_gestor, reservas["propria"], {"situacao": "CONFIRMADA"})
    _alterar(cliente_gestor, reservas["propria"], {"situacao": "CONCLUIDA"})

    # Act
    reserva = cliente_solicitante.get(_url_detalhe(reservas["propria"])).data["dados"]

    # Assert
    assert reserva["situacao"] == "CONCLUIDA"
    assert reserva["acoes_disponiveis"] == []


def test_resposta_da_solicitacao_traz_as_acoes_de_quem_solicitou(
    cliente_solicitante, espaco_id
):
    # Act
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

    # Assert
    assert _rotulos_das_acoes(resposta.data["dados"]) == ["Cancelar"]


def test_gestor_tambem_solicita_reserva(cliente_gestor, usuario_gestor, espaco_id):
    # Act
    reserva_id = _solicitar(cliente_gestor, espaco_id, "16:00", "17:00")

    # Assert
    reserva = cliente_gestor.get(_url_detalhe(reserva_id)).data["dados"]
    assert reserva["solicitante"]["usuario_id"] == usuario_gestor.pk
    assert reserva["situacao"] == "SOLICITADA"
