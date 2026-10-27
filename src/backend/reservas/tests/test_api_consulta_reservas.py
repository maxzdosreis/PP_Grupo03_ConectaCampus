from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from reservas.api.serializers import ReservaSaidaSerializer
from reservas.application.repositorio import FiltrosDeReservas
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango

pytestmark = pytest.mark.django_db

URL_RESERVAS = reverse("reservas:lista")
URL_ESPACOS = reverse("espacos:lista")
URL_SITUACOES = reverse("reservas:situacoes")
SENHA = "senha-de-teste-123"
ID_INEXISTENTE = 9999
ORDEM_POR_INICIO = ["R4", "R1", "R3", "R2"]


def _url_detalhe(reserva_id):
    return reverse("reservas:detalhe", args=[reserva_id])


def _dia(deslocamento):
    return timezone.localdate() + timedelta(days=deslocamento)


def _criar_usuario(email, nome, matricula):
    return get_user_model().objects.create_user(
        email, SENHA, nome=nome, matricula=matricula
    )


def _cliente_de(usuario):
    cliente = APIClient()
    cliente.force_authenticate(user=usuario)
    return cliente


def _cadastrar_espaco(cliente, nome, tipo):
    resposta = cliente.post(
        URL_ESPACOS, {"nome": nome, "tipo": tipo, "capacidade": 20}, format="json"
    )
    return resposta.data["dados"]["id"]


def _solicitar(cliente, espaco_id, dia, hora_inicio, hora_fim):
    resposta = cliente.post(
        URL_RESERVAS,
        {
            "espaco_id": espaco_id,
            "data": dia.isoformat(),
            "hora_inicio": hora_inicio,
            "hora_fim": hora_fim,
            "finalidade": "Treino",
        },
        format="json",
    )
    return resposta.data["dados"]["id"]


def _alterar_situacao(reserva_id, situacao, motivo=None):
    repositorio = RepositorioReservasDjango()
    reserva = repositorio.obter_por_id(reserva_id)
    reserva.alterar_situacao(situacao, motivo=motivo)
    repositorio.salvar(reserva)


@pytest.fixture
def ana():
    return _criar_usuario("ana@exemplo.com", "Ana Souza", "2026001")


@pytest.fixture
def bruno():
    return _criar_usuario("bruno@exemplo.com", "Bruno Lima", "2026002")


@pytest.fixture
def cliente(ana):
    return _cliente_de(ana)


@pytest.fixture
def massa(cliente, bruno):
    """Quatro reservas criadas fora da ordem de início (R4, R1, R3, R2)."""
    cliente_bruno = _cliente_de(bruno)
    quadra = _cadastrar_espaco(cliente, "Quadra Coberta", "QUADRA_POLIESPORTIVA")
    campo = _cadastrar_espaco(cliente, "Campo Norte", "CAMPO_DE_FUTEBOL")
    r1 = _solicitar(cliente, quadra, _dia(1), "10:00", "11:00")
    r2 = _solicitar(cliente, campo, _dia(2), "08:00", "09:00")
    r3 = _solicitar(cliente_bruno, quadra, _dia(1), "14:00", "15:00")
    r4 = _solicitar(cliente_bruno, campo, _dia(1), "09:00", "10:00")
    _alterar_situacao(r2, SituacaoReserva.CONFIRMADA)
    _alterar_situacao(r3, SituacaoReserva.CONFIRMADA)
    _alterar_situacao(r4, SituacaoReserva.CANCELADA, motivo="Chuva forte")
    return {"quadra": quadra, "campo": campo, "R1": r1, "R2": r2, "R3": r3, "R4": r4}


def _consultar(cliente, parametros=None):
    return cliente.get(URL_RESERVAS, parametros or {})


def _ids_de(resposta):
    return [reserva["id"] for reserva in resposta.data["dados"]]


def _ids_esperados(massa, nomes):
    return [massa[nome] for nome in nomes]


def _retrato_das_reservas():
    reservas = RepositorioReservasDjango().listar(FiltrosDeReservas())
    return ReservaSaidaSerializer(reservas, many=True).data


def test_consulta_sem_login_responde_401(massa):
    # Act
    resposta = _consultar(APIClient())

    # Assert
    assert resposta.status_code == 401
    assert resposta.data["erro"]["codigo"] == "NAO_AUTENTICADO"


def test_consulta_sem_filtros_devolve_todas_ordenadas_por_inicio(cliente, massa):
    # Act
    resposta = _consultar(cliente)

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "4 reservas encontradas."
    assert _ids_de(resposta) == _ids_esperados(massa, ORDEM_POR_INICIO)


@pytest.mark.parametrize(
    ("parametros", "esperadas"),
    [
        (lambda m: {"espaco": m["quadra"]}, ["R1", "R3"]),
        (lambda m: {"situacao": "CONFIRMADA"}, ["R3", "R2"]),
        (lambda m: {"data": _dia(2).isoformat()}, ["R2"]),
        (lambda m: {"solicitante": "bRUNO"}, ["R4", "R3"]),
        (lambda m: {"solicitante": "001"}, ["R1", "R2"]),
        (lambda m: {"minhas": "true"}, ["R1", "R2"]),
    ],
    ids=[
        "espaco",
        "situacao",
        "data",
        "trecho-do-nome-em-outra-caixa",
        "trecho-da-matricula",
        "minhas",
    ],
)
def test_cada_criterio_sozinho_devolve_so_as_correspondentes(
    cliente, massa, parametros, esperadas
):
    # Act
    resposta = _consultar(cliente, parametros(massa))

    # Assert
    assert resposta.status_code == 200
    assert _ids_de(resposta) == _ids_esperados(massa, esperadas)


@pytest.mark.parametrize(
    ("parametros", "esperadas"),
    [
        (lambda m: {"espaco": m["quadra"], "situacao": "CONFIRMADA"}, ["R3"]),
        (lambda m: {"data": _dia(1).isoformat(), "solicitante": "ana"}, ["R1"]),
        (lambda m: {"minhas": "true", "situacao": "CONFIRMADA"}, ["R2"]),
        (
            lambda m: {
                "espaco": m["quadra"],
                "situacao": "SOLICITADA",
                "data": _dia(1).isoformat(),
                "solicitante": "souza",
            },
            ["R1"],
        ),
        (lambda m: {"espaco": m["campo"], "situacao": "SOLICITADA"}, []),
    ],
    ids=[
        "espaco-e-situacao",
        "data-e-solicitante",
        "minhas-e-situacao",
        "quatro-criterios",
        "combinacao-sem-resultado",
    ],
)
def test_criterios_combinados_se_somam(cliente, massa, parametros, esperadas):
    # Act
    resposta = _consultar(cliente, parametros(massa))

    # Assert
    assert resposta.status_code == 200
    assert _ids_de(resposta) == _ids_esperados(massa, esperadas)


@pytest.mark.parametrize(
    "parametros",
    [{"solicitante": "   "}, {"situacao": ""}],
    ids=["solicitante-em-branco", "situacao-em-branco"],
)
def test_filtro_em_branco_e_ignorado(cliente, massa, parametros):
    # Act
    resposta = _consultar(cliente, parametros)

    # Assert
    assert resposta.status_code == 200
    assert _ids_de(resposta) == _ids_esperados(massa, ORDEM_POR_INICIO)


@pytest.mark.parametrize(
    ("parametros", "campo"),
    [
        ({"situacao": "PENDENTE"}, "situacao"),
        ({"data": "2026-13-40"}, "data"),
        ({"espaco": "abc"}, "espaco"),
        ({"espaco": "0"}, "espaco"),
    ],
    ids=["situacao-fora-da-lista", "data-inexistente", "espaco-texto", "espaco-zero"],
)
def test_filtro_invalido_responde_400_com_o_campo(cliente, massa, parametros, campo):
    # Act
    resposta = _consultar(cliente, parametros)

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "DADOS_INVALIDOS"
    assert campo in resposta.data["erro"]["campos"]


def test_espaco_inexistente_no_filtro_devolve_lista_vazia(cliente, massa):
    # Act
    resposta = _consultar(cliente, {"espaco": ID_INEXISTENTE})

    # Assert
    assert resposta.status_code == 200
    assert resposta.data == {"mensagem": "Nenhuma reserva encontrada.", "dados": []}


@pytest.mark.parametrize(
    ("parametros", "mensagem"),
    [
        ({"espaco": ID_INEXISTENTE}, "Nenhuma reserva encontrada."),
        ({"data": _dia(2).isoformat()}, "1 reserva encontrada."),
        ({}, "4 reservas encontradas."),
    ],
    ids=["nenhuma", "uma", "varias"],
)
def test_mensagem_informa_a_quantidade_encontrada(cliente, massa, parametros, mensagem):
    # Act
    resposta = _consultar(cliente, parametros)

    # Assert
    assert resposta.data["mensagem"] == mensagem


def test_consulta_nao_altera_as_reservas(cliente, massa):
    # Arrange
    antes = _retrato_das_reservas()

    # Act
    _consultar(cliente)
    _consultar(cliente, {"situacao": "CONFIRMADA", "espaco": massa["quadra"]})
    _consultar(cliente, {"minhas": "true", "solicitante": "ana"})
    _consultar(cliente, {"situacao": "PENDENTE"})
    cliente.get(_url_detalhe(massa["R1"]))

    # Assert
    assert _retrato_das_reservas() == antes


def test_detalhe_devolve_a_reserva_no_mesmo_formato_da_criacao(cliente, bruno, massa):
    # Act
    resposta = cliente.get(_url_detalhe(massa["R4"]))

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Reserva encontrada."
    dados = resposta.data["dados"]
    assert dados["criada_em"].endswith("-03:00")
    assert dados == {
        "id": massa["R4"],
        "espaco_id": massa["campo"],
        "solicitante": {
            "usuario_id": bruno.pk,
            "nome": "Bruno Lima",
            "matricula": "2026002",
        },
        "data": _dia(1).isoformat(),
        "hora_inicio": "09:00",
        "hora_fim": "10:00",
        "finalidade": "Treino",
        "situacao": "CANCELADA",
        "situacao_rotulo": "Cancelada",
        "motivo_da_situacao": "Chuva forte",
        "criada_em": dados["criada_em"],
        "acoes_disponiveis": [],
    }


def test_detalhe_inexistente_responde_404(cliente):
    # Act
    resposta = cliente.get(_url_detalhe(ID_INEXISTENTE))

    # Assert
    assert resposta.status_code == 404
    assert resposta.data == {
        "erro": {
            "codigo": "RESERVA_NAO_ENCONTRADA",
            "mensagem": f"Reserva de código {ID_INEXISTENTE} não encontrada.",
        }
    }


def test_detalhe_sem_login_responde_401(massa):
    # Act
    resposta = APIClient().get(_url_detalhe(massa["R1"]))

    # Assert
    assert resposta.status_code == 401
    assert resposta.data["erro"]["codigo"] == "NAO_AUTENTICADO"


def test_situacoes_de_reserva_listam_todas_na_ordem_do_enum_sem_login():
    # Act
    resposta = APIClient().get(URL_SITUACOES)

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Situações de reserva disponíveis."
    assert resposta.data["dados"][0] == {"valor": "SOLICITADA", "rotulo": "Solicitada"}
    assert resposta.data["dados"] == [
        {"valor": situacao.value, "rotulo": situacao.rotulo}
        for situacao in SituacaoReserva
    ]
