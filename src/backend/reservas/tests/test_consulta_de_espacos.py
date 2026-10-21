import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from compartilhado.api.tratador_de_erros import tratar_excecao
from compartilhado.domain.erros import ConflitoDeEstado, RecursoNaoEncontrado
from reservas.application.portas import EspacoReservavel
from reservas.infrastructure.consulta_de_espacos import ConsultaDeEspacosViaFachada

ID_INEXISTENTE = 9999


def _cadastrar_espaco_pela_api(nome):
    resposta = APIClient().post(
        reverse("espacos:lista"),
        {"nome": nome, "tipo": "GINASIO", "capacidade": 30},
        format="json",
    )
    assert resposta.status_code == 201
    return resposta.data["dados"]


@pytest.mark.django_db
def test_espaco_ativo_cadastrado_pela_api_vira_espaco_reservavel():
    # Arrange
    cadastrado = _cadastrar_espaco_pela_api("Ginásio Central")

    # Act
    espaco = ConsultaDeEspacosViaFachada().obter_espaco_reservavel(cadastrado["id"])

    # Assert
    assert espaco == EspacoReservavel(id=cadastrado["id"], nome="Ginásio Central")


@pytest.mark.django_db
def test_espaco_inexistente_sobe_recurso_nao_encontrado_tratado_como_404():
    # Act
    with pytest.raises(RecursoNaoEncontrado) as erro:
        ConsultaDeEspacosViaFachada().obter_espaco_reservavel(ID_INEXISTENTE)
    resposta = tratar_excecao(erro.value, {})

    # Assert
    assert resposta.status_code == 404
    assert resposta.data["erro"]["codigo"] == "ESPACO_NAO_ENCONTRADO"


def test_erro_da_fachada_sobe_sem_alteracao(monkeypatch):
    # Arrange
    original = ConflitoDeEstado("Este espaço está inativo e não aceita reservas.")

    def _fachada_que_falha(_espaco_id):
        raise original

    monkeypatch.setattr(
        "espacos.publico.verificar_espaco_disponivel", _fachada_que_falha
    )

    # Act
    with pytest.raises(ConflitoDeEstado) as erro:
        ConsultaDeEspacosViaFachada().obter_espaco_reservavel(1)

    # Assert
    assert erro.value is original
