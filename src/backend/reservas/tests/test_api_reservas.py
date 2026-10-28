import base64
from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from reservas.application.repositorio import FiltrosDeReservas
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango

pytestmark = pytest.mark.django_db

URL_RESERVAS = reverse("reservas:lista")
EMAIL = "ana@exemplo.com"
SENHA = "senha-de-teste-123"
ID_INEXISTENTE = 9999


@pytest.fixture
def usuario(usuario_solicitante):
    return usuario_solicitante


@pytest.fixture
def cliente(cliente_solicitante):
    return cliente_solicitante


def _amanha():
    return timezone.localdate() + timedelta(days=1)


def _ontem():
    return timezone.localdate() - timedelta(days=1)


def _dados_validos(espaco_id, **sobrescritas):
    dados = {
        "espaco_id": espaco_id,
        "data": _amanha().isoformat(),
        "hora_inicio": "10:00",
        "hora_fim": "11:00",
        "finalidade": "Treino de vôlei",
    }
    dados.update(sobrescritas)
    return dados


def _solicitar(cliente, corpo):
    return cliente.post(URL_RESERVAS, corpo, format="json")


def _quantidade_de_reservas():
    return len(RepositorioReservasDjango().listar(FiltrosDeReservas()))


def _solicitante_de(usuario):
    return {"usuario_id": usuario.pk, "nome": "Ana Souza", "matricula": "2026001"}


def test_solicitacao_valida_responde_201_com_a_reserva(cliente, usuario, espaco_id):
    # Act
    resposta = _solicitar(cliente, _dados_validos(espaco_id))

    # Assert
    assert resposta.status_code == 201
    assert set(resposta.data) == {"mensagem", "dados"}
    assert resposta.data["mensagem"] == (
        "Reserva solicitada com sucesso. Aguarde a confirmação do gestor."
    )
    dados = resposta.data["dados"]
    assert isinstance(dados["id"], int)
    assert dados["criada_em"].endswith("-03:00")
    assert dados == {
        "id": dados["id"],
        "espaco_id": espaco_id,
        "solicitante": _solicitante_de(usuario),
        "data": _amanha().isoformat(),
        "hora_inicio": "10:00",
        "hora_fim": "11:00",
        "finalidade": "Treino de vôlei",
        "situacao": "SOLICITADA",
        "situacao_rotulo": "Solicitada",
        "motivo_da_situacao": None,
        "criada_em": dados["criada_em"],
        "acoes_disponiveis": [
            {"situacao": "CANCELADA", "rotulo": "Cancelar", "exige_motivo": True},
        ],
    }
    assert _quantidade_de_reservas() == 1


def test_solicitante_enviado_no_corpo_e_ignorado(cliente, usuario, espaco_id):
    # Arrange
    falso = {"usuario_id": 999, "nome": "Outra Pessoa", "matricula": "0000000"}

    # Act
    resposta = _solicitar(cliente, _dados_validos(espaco_id, solicitante=falso))

    # Assert
    assert resposta.status_code == 201
    assert resposta.data["dados"]["solicitante"] == _solicitante_de(usuario)


def test_solicitacao_sem_login_responde_401(espaco_id):
    # Act
    resposta = _solicitar(APIClient(), _dados_validos(espaco_id))

    # Assert
    assert resposta.status_code == 401
    assert resposta.data["erro"]["codigo"] == "NAO_AUTENTICADO"
    assert _quantidade_de_reservas() == 0


def test_campos_ausentes_respondem_400_com_cada_campo(cliente):
    # Act
    resposta = _solicitar(cliente, {})

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "DADOS_INVALIDOS"
    assert set(resposta.data["erro"]["campos"]) == {
        "espaco_id",
        "data",
        "hora_inicio",
        "hora_fim",
        "finalidade",
    }


@pytest.mark.parametrize(
    ("sobrescritas", "codigo", "campo"),
    [
        ({"data": "2026-13-40"}, "DADOS_INVALIDOS", "data"),
        ({"hora_inicio": "11:00", "hora_fim": "10:00"}, "HORARIO_INVALIDO", "hora_fim"),
        ({"data": _ontem().isoformat()}, "DATA_RETROATIVA", "data"),
        ({"finalidade": "   "}, "CAMPO_OBRIGATORIO_AUSENTE", "finalidade"),
    ],
    ids=[
        "data-inexistente",
        "fim-antes-do-inicio",
        "data-retroativa",
        "sem-finalidade",
    ],
)
def test_dado_invalido_responde_400_sem_salvar(
    cliente, espaco_id, sobrescritas, codigo, campo
):
    # Act
    resposta = _solicitar(cliente, _dados_validos(espaco_id, **sobrescritas))

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == codigo
    assert campo in resposta.data["erro"]["campos"]
    assert _quantidade_de_reservas() == 0


def test_espaco_inexistente_responde_404(cliente):
    # Act
    resposta = _solicitar(cliente, _dados_validos(ID_INEXISTENTE))

    # Assert
    assert resposta.status_code == 404
    assert resposta.data == {
        "erro": {
            "codigo": "ESPACO_NAO_ENCONTRADO",
            "mensagem": f"Espaço de código {ID_INEXISTENTE} não encontrado.",
        }
    }
    assert _quantidade_de_reservas() == 0


def test_horario_ocupado_responde_409_e_preserva_as_reservas(cliente, espaco_id):
    # Arrange
    _solicitar(cliente, _dados_validos(espaco_id))

    # Act
    resposta = _solicitar(
        cliente, _dados_validos(espaco_id, hora_inicio="10:30", hora_fim="11:30")
    )

    # Assert
    assert resposta.status_code == 409
    assert resposta.data["erro"]["codigo"] == "CONFLITO_DE_HORARIO"
    assert "Solicitada" in resposta.data["erro"]["mensagem"]
    assert _quantidade_de_reservas() == 1


def test_token_jwt_do_login_autoriza_solicitacao(usuario, espaco_id):
    # Arrange
    login = APIClient().post(
        reverse("contas:login"), {"email": EMAIL, "senha": SENHA}, format="json"
    )
    cliente = APIClient()
    cliente.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['dados']['access']}")

    # Act
    resposta = _solicitar(cliente, _dados_validos(espaco_id))

    # Assert
    assert resposta.status_code == 201
    assert resposta.data["dados"]["solicitante"]["usuario_id"] == usuario.pk


def test_autenticacao_basic_nao_e_mais_aceita(usuario, espaco_id):
    # Arrange
    credenciais = base64.b64encode(f"{EMAIL}:{SENHA}".encode()).decode()
    cliente = APIClient()
    cliente.credentials(HTTP_AUTHORIZATION=f"Basic {credenciais}")

    # Act
    resposta = _solicitar(cliente, _dados_validos(espaco_id))

    # Assert
    assert resposta.status_code == 401
    assert resposta.data["erro"]["codigo"] == "NAO_AUTENTICADO"
    assert _quantidade_de_reservas() == 0
