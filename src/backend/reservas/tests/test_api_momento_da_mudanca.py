from datetime import datetime, time, timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from reservas.domain.intervalo_de_horario import FUSO_HORARIO

pytestmark = pytest.mark.django_db

URL_RESERVAS = reverse("reservas:lista")
MOTIVO = "Chuva forte"
MICROSSEGUNDO = timedelta(microseconds=1)


def _dia():
    return timezone.localdate() + timedelta(days=1)


def _inicio():
    return datetime.combine(_dia(), time(10, 0), FUSO_HORARIO)


def _termino():
    return datetime.combine(_dia(), time(11, 0), FUSO_HORARIO)


def _solicitar(cliente, espaco_id, inicio="10:00", fim="11:00"):
    resposta = cliente.post(
        URL_RESERVAS,
        {
            "espaco_id": espaco_id,
            "data": _dia().isoformat(),
            "hora_inicio": inicio,
            "hora_fim": fim,
            "finalidade": "Treino",
        },
        format="json",
    )
    return resposta.data["dados"]["id"]


def _alterar(cliente, reserva_id, situacao, motivo=None):
    corpo = {"situacao": situacao}
    if motivo:
        corpo["motivo"] = motivo
    return cliente.patch(
        reverse("reservas:situacao", args=[reserva_id]), corpo, format="json"
    )


def _detalhe(cliente, reserva_id):
    return cliente.get(reverse("reservas:detalhe", args=[reserva_id])).data["dados"]


def _acoes(reserva):
    return [acao["situacao"] for acao in reserva["acoes_disponiveis"]]


@pytest.fixture
def reserva_id(cliente_solicitante, espaco_id):
    return _solicitar(cliente_solicitante, espaco_id)


@pytest.fixture
def confirmada_id(cliente_gestor, reserva_id):
    _alterar(cliente_gestor, reserva_id, "CONFIRMADA")
    return reserva_id


def test_concluir_antes_do_termino_responde_409_com_codigo_proprio(
    cliente_gestor, confirmada_id, relogio_da_api
):
    # Arrange
    relogio_da_api(_termino() - MICROSSEGUNDO)

    # Act
    resposta = _alterar(cliente_gestor, confirmada_id, "CONCLUIDA")

    # Assert
    assert resposta.status_code == 409
    assert resposta.data == {
        "erro": {
            "codigo": "CONCLUSAO_ANTES_DO_TERMINO",
            "mensagem": "Só é possível concluir a reserva a partir do término "
            f"dela ({_dia():%d/%m/%Y} às 11:00).",
        }
    }
    assert _detalhe(cliente_gestor, confirmada_id)["situacao"] == "CONFIRMADA"


def test_concluir_no_instante_do_termino_funciona(
    cliente_gestor, confirmada_id, relogio_da_api
):
    # Arrange
    relogio_da_api(_termino())

    # Act
    resposta = _alterar(cliente_gestor, confirmada_id, "CONCLUIDA")

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Reserva concluída com sucesso."
    assert resposta.data["dados"]["acoes_disponiveis"] == []


@pytest.mark.parametrize("situacao", ["RECUSADA", "CANCELADA"])
def test_recusar_ou_cancelar_no_instante_do_inicio_responde_409(
    cliente_gestor, reserva_id, relogio_da_api, situacao
):
    # Arrange
    relogio_da_api(_inicio())

    # Act
    resposta = _alterar(cliente_gestor, reserva_id, situacao, MOTIVO)

    # Assert
    assert resposta.status_code == 409
    assert resposta.data["erro"]["codigo"] == "RECUSA_OU_CANCELAMENTO_APOS_O_INICIO"
    assert "antes do início" in resposta.data["erro"]["mensagem"]
    assert _detalhe(cliente_gestor, reserva_id)["situacao"] == "SOLICITADA"


@pytest.mark.parametrize("situacao", ["RECUSADA", "CANCELADA"])
def test_recusar_ou_cancelar_antes_do_inicio_funciona(
    cliente_gestor, reserva_id, relogio_da_api, situacao
):
    # Arrange
    relogio_da_api(_inicio() - MICROSSEGUNDO)

    # Act
    resposta = _alterar(cliente_gestor, reserva_id, situacao, MOTIVO)

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"]["situacao"] == situacao


def test_cancelar_confirmada_depois_do_inicio_o_gestor_nao_pode(
    cliente_gestor, confirmada_id, relogio_da_api
):
    # Arrange
    relogio_da_api(_inicio() + timedelta(minutes=10))

    # Act
    resposta = _alterar(cliente_gestor, confirmada_id, "CANCELADA", MOTIVO)

    # Assert
    assert resposta.status_code == 409
    assert resposta.data["erro"]["codigo"] == "RECUSA_OU_CANCELAMENTO_APOS_O_INICIO"


def test_solicitante_cancela_a_propria_depois_do_inicio_como_antes(
    cliente_solicitante, confirmada_id, relogio_da_api
):
    # Arrange
    relogio_da_api(_termino() + timedelta(hours=3))

    # Act
    resposta = _alterar(cliente_solicitante, confirmada_id, "CANCELADA", MOTIVO)

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"]["situacao"] == "CANCELADA"


def test_gestor_confirma_depois_do_inicio_como_antes(
    cliente_gestor, reserva_id, relogio_da_api
):
    # Arrange
    relogio_da_api(_inicio() + timedelta(minutes=10))

    # Act
    resposta = _alterar(cliente_gestor, reserva_id, "CONFIRMADA")

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"]["situacao"] == "CONFIRMADA"


def test_acoes_do_gestor_acompanham_a_janela_da_reserva(
    cliente_gestor, confirmada_id, relogio_da_api
):
    # Act / Assert
    relogio_da_api(_inicio() - MICROSSEGUNDO)
    assert _acoes(_detalhe(cliente_gestor, confirmada_id)) == ["CANCELADA"]
    relogio_da_api(_inicio())
    assert _acoes(_detalhe(cliente_gestor, confirmada_id)) == []
    relogio_da_api(_termino() - MICROSSEGUNDO)
    assert _acoes(_detalhe(cliente_gestor, confirmada_id)) == []
    relogio_da_api(_termino())
    assert _acoes(_detalhe(cliente_gestor, confirmada_id)) == ["CONCLUIDA"]


def test_solicitante_mantem_cancelar_em_qualquer_momento(
    cliente_solicitante, confirmada_id, relogio_da_api
):
    # Arrange
    momentos = (
        _inicio() - timedelta(days=1),
        _inicio(),
        _termino() + timedelta(days=1),
    )

    # Act / Assert
    for momento in momentos:
        relogio_da_api(momento)
        assert _acoes(_detalhe(cliente_solicitante, confirmada_id)) == ["CANCELADA"]


def test_a_lista_usa_um_unico_instante_para_todas_as_reservas(
    cliente_gestor, cliente_solicitante, espaco_id, monkeypatch
):
    # Arrange
    _solicitar(cliente_solicitante, espaco_id, "10:00", "11:00")
    _solicitar(cliente_solicitante, espaco_id, "12:00", "13:00")
    chamadas = []

    def relogio_que_avanca():
        chamadas.append(1)
        return _inicio() - timedelta(minutes=1) + timedelta(hours=len(chamadas) - 1)

    monkeypatch.setattr("reservas.api.dependencias.agora", relogio_que_avanca)

    # Act
    resposta = cliente_gestor.get(URL_RESERVAS)

    # Assert
    assert len(chamadas) == 1
    assert [_acoes(r) for r in resposta.data["dados"]] == [
        ["CONFIRMADA", "RECUSADA", "CANCELADA"]
    ] * 2


def test_o_patch_usa_o_mesmo_instante_na_decisao_e_na_resposta(
    cliente_gestor, reserva_id, monkeypatch
):
    # Arrange
    chamadas = []

    def relogio_que_avanca():
        chamadas.append(1)
        return _inicio() - timedelta(minutes=1) + timedelta(hours=len(chamadas) - 1)

    monkeypatch.setattr("reservas.api.dependencias.agora", relogio_que_avanca)

    # Act
    resposta = _alterar(cliente_gestor, reserva_id, "CONFIRMADA")

    # Assert
    assert len(chamadas) == 1
    assert resposta.data["dados"]["situacao"] == "CONFIRMADA"
