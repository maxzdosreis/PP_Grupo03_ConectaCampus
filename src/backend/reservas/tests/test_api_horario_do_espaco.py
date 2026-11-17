from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

pytestmark = pytest.mark.django_db

URL_ESPACOS = reverse("espacos:lista")
URL_RESERVAS = reverse("reservas:lista")
URL_OCUPACAO = reverse("reservas:ocupacao")
FINALIDADE = "Treino do time de vôlei"


def _amanha():
    return timezone.localdate() + timedelta(days=1)


def _cadastrar_espaco(cliente_gestor, nome, **horario):
    resposta = cliente_gestor.post(
        URL_ESPACOS,
        {"nome": nome, "tipo": "GINASIO", "capacidade": 30, **horario},
        format="json",
    )
    assert resposta.status_code == 201
    return resposta.data["dados"]["id"]


def _solicitar(cliente, espaco_id, inicio, fim, data=None):
    return cliente.post(
        URL_RESERVAS,
        {
            "espaco_id": espaco_id,
            "data": (data or _amanha()).isoformat(),
            "hora_inicio": inicio,
            "hora_fim": fim,
            "finalidade": FINALIDADE,
        },
        format="json",
    )


@pytest.fixture
def espaco_padrao(cliente_gestor):
    return _cadastrar_espaco(cliente_gestor, "Ginásio Padrão")


@pytest.fixture
def espaco_ate_as_22(cliente_gestor):
    return _cadastrar_espaco(
        cliente_gestor, "Ginásio de Dia", abertura="08:00", fechamento="22:00"
    )


def test_pedido_das_23_as_00_no_horario_padrao_e_aceito_e_termina_a_meia_noite(
    cliente_solicitante, espaco_padrao
):
    # Act
    resposta = _solicitar(cliente_solicitante, espaco_padrao, "23:00", "00:00")

    # Assert
    assert resposta.status_code == 201
    dados = resposta.data["dados"]
    assert dados["situacao"] == "SOLICITADA"
    assert dados["data"] == _amanha().isoformat()
    assert (dados["hora_inicio"], dados["hora_fim"]) == ("23:00", "00:00")


def test_pedido_depois_das_22_no_horario_padrao_e_aceito(
    cliente_solicitante, espaco_padrao
):
    # Act
    resposta = _solicitar(cliente_solicitante, espaco_padrao, "22:00", "23:00")

    # Assert
    assert resposta.status_code == 201


@pytest.mark.parametrize(
    ("inicio", "fim", "campo"),
    [("06:59", "08:00", "hora_inicio"), ("00:00", "01:00", "hora_inicio")],
    ids=["06h59", "inicio-a-meia-noite"],
)
def test_pedido_que_comeca_antes_da_abertura_e_recusado_no_horario_padrao(
    cliente_solicitante, espaco_padrao, inicio, fim, campo
):
    # Act
    resposta = _solicitar(cliente_solicitante, espaco_padrao, inicio, fim)

    # Assert
    assert resposta.status_code == 400
    erro = resposta.data["erro"]
    assert erro["codigo"] == "FORA_DO_HORARIO_DE_FUNCIONAMENTO"
    assert erro["mensagem"] == (
        "O espaço funciona das 07:00 às 00:00. Escolha um horário dentro desse período."
    )
    assert campo in erro["campos"]


def test_pedido_das_23h30_as_00h30_nao_vira_o_dia_e_e_recusado(
    cliente_solicitante, espaco_padrao
):
    # Act
    resposta = _solicitar(cliente_solicitante, espaco_padrao, "23:30", "00:30")

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "HORARIO_INVALIDO"


def test_pedido_fora_do_horario_do_espaco_cita_o_horario_dele(
    cliente_solicitante, espaco_ate_as_22
):
    # Act
    resposta = _solicitar(cliente_solicitante, espaco_ate_as_22, "22:30", "23:00")

    # Assert
    assert resposta.status_code == 400
    erro = resposta.data["erro"]
    assert erro["codigo"] == "FORA_DO_HORARIO_DE_FUNCIONAMENTO"
    assert erro["mensagem"] == (
        "O espaço funciona das 08:00 às 22:00. Escolha um horário dentro desse período."
    )
    assert "hora_inicio" not in erro["campos"]
    assert "hora_fim" in erro["campos"]


def test_pedido_que_passa_do_fechamento_do_espaco_e_recusado_junto_ao_termino(
    cliente_gestor, cliente_solicitante
):
    # Arrange
    espaco = _cadastrar_espaco(
        cliente_gestor, "Quadra do Dia", abertura="08:00", fechamento="18:00"
    )

    # Act
    resposta = _solicitar(cliente_solicitante, espaco, "17:30", "18:30")

    # Assert
    assert resposta.status_code == 400
    assert "hora_fim" in resposta.data["erro"]["campos"]
    assert "08:00 às 18:00" in resposta.data["erro"]["mensagem"]
    listagem = cliente_solicitante.get(URL_RESERVAS).data["dados"]
    assert listagem == []


def test_limites_de_duracao_continuam_os_mesmos_no_horario_padrao(
    cliente_solicitante, espaco_padrao
):
    # Act
    curta = _solicitar(cliente_solicitante, espaco_padrao, "10:00", "10:20")
    longa = _solicitar(cliente_solicitante, espaco_padrao, "10:00", "13:01")
    no_limite = _solicitar(cliente_solicitante, espaco_padrao, "10:00", "13:00")

    # Assert
    for recusada in (curta, longa):
        assert recusada.status_code == 400
        assert recusada.data["erro"]["codigo"] == "DURACAO_INVALIDA"
        assert recusada.data["erro"]["mensagem"] == (
            "A reserva deve durar entre 30 minutos e 3 horas."
        )
    assert no_limite.status_code == 201


def test_espaco_inexistente_e_404_mesmo_com_horario_invalido(cliente_solicitante):
    # Act
    resposta = _solicitar(cliente_solicitante, 9999, "06:00", "06:10")

    # Assert
    assert resposta.status_code == 404
    assert resposta.data["erro"]["codigo"] == "ESPACO_NAO_ENCONTRADO"


def test_agenda_do_dia_usa_o_horario_do_espaco(cliente_solicitante, espaco_ate_as_22):
    # Arrange
    assert (
        _solicitar(cliente_solicitante, espaco_ate_as_22, "12:00", "13:00").status_code
        == 201
    )

    # Act
    resposta = cliente_solicitante.get(
        URL_OCUPACAO, {"espaco": espaco_ate_as_22, "data": _amanha().isoformat()}
    )

    # Assert
    dados = resposta.data["dados"]
    assert (dados["horario_de_abertura"], dados["horario_de_fechamento"]) == (
        "08:00",
        "22:00",
    )
    assert dados["livres"] == [
        {"hora_inicio": "08:00", "hora_fim": "12:00"},
        {"hora_inicio": "13:00", "hora_fim": "22:00"},
    ]


def test_reserva_das_23_as_00_aparece_so_na_agenda_do_dia_certo(
    cliente_solicitante, espaco_padrao
):
    # Arrange
    assert (
        _solicitar(cliente_solicitante, espaco_padrao, "23:00", "00:00").status_code
        == 201
    )

    # Act
    do_dia = cliente_solicitante.get(
        URL_OCUPACAO, {"espaco": espaco_padrao, "data": _amanha().isoformat()}
    ).data["dados"]
    do_seguinte = cliente_solicitante.get(
        URL_OCUPACAO,
        {"espaco": espaco_padrao, "data": (_amanha() + timedelta(days=1)).isoformat()},
    ).data["dados"]

    # Assert
    assert [(o["hora_inicio"], o["hora_fim"]) for o in do_dia["ocupados"]] == [
        ("23:00", "00:00")
    ]
    assert do_dia["livres"] == [{"hora_inicio": "07:00", "hora_fim": "23:00"}]
    assert do_seguinte["ocupados"] == []
    assert do_seguinte["livres"] == [{"hora_inicio": "07:00", "hora_fim": "00:00"}]


def test_conflito_na_virada_so_vale_para_o_mesmo_dia_local(
    cliente_solicitante, espaco_padrao
):
    # Arrange
    assert (
        _solicitar(cliente_solicitante, espaco_padrao, "23:00", "00:00").status_code
        == 201
    )

    # Act
    mesmo_horario = _solicitar(cliente_solicitante, espaco_padrao, "23:30", "00:00")
    dia_seguinte = _solicitar(
        cliente_solicitante,
        espaco_padrao,
        "00:00",
        "01:00",
        data=_amanha() + timedelta(days=1),
    )

    # Assert
    assert mesmo_horario.status_code == 409
    assert mesmo_horario.data["erro"]["codigo"] == "CONFLITO_DE_HORARIO"
    assert dia_seguinte.status_code == 400
    assert dia_seguinte.data["erro"]["codigo"] == "FORA_DO_HORARIO_DE_FUNCIONAMENTO"


def test_regras_de_agenda_trazem_a_duracao_sugerida_de_1_hora(cliente_solicitante):
    # Act
    dados = cliente_solicitante.get(reverse("reservas:regras_de_agenda")).data["dados"]

    # Assert
    assert dados["duracao_sugerida_em_minutos"] == 60
    assert dados["duracao_minima_em_minutos"] == 30
    assert dados["duracao_maxima_em_minutos"] == 180
    assert dados["antecedencia_maxima_em_dias"] == 30
