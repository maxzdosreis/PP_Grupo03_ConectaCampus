from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from espacos.tests.fakes import dados_validos

pytestmark = pytest.mark.django_db

URL_LISTA = reverse("espacos:lista")
URL_RESERVAS = reverse("reservas:lista")
CAMPOS_DE_SEMPRE = {"id", "nome", "tipo", "tipo_rotulo", "capacidade", "ativo"}


def _detalhe(espaco_id):
    return reverse("espacos:detalhe", args=[espaco_id])


def _cadastrar(cliente, **sobrescritas):
    return cliente.post(URL_LISTA, dados_validos(**sobrescritas), format="json")


def _amanha():
    return timezone.localdate() + timedelta(days=1)


def _solicitar(cliente, espaco_id, inicio, fim):
    return cliente.post(
        URL_RESERVAS,
        {
            "espaco_id": espaco_id,
            "data": _amanha().isoformat(),
            "hora_inicio": inicio,
            "hora_fim": fim,
            "finalidade": "Treino do time",
        },
        format="json",
    )


def test_cadastrar_sem_horario_grava_o_padrao_das_07_as_00_00(cliente_gestor):
    # Act
    resposta = _cadastrar(cliente_gestor)

    # Assert
    assert resposta.status_code == 201
    assert resposta.data["dados"]["abertura"] == "07:00"
    assert resposta.data["dados"]["fechamento"] == "00:00"


def test_cadastrar_com_horario_proprio_devolve_o_horario(cliente_gestor):
    # Act
    resposta = _cadastrar(cliente_gestor, abertura="08:00", fechamento="22:00")

    # Assert
    assert resposta.status_code == 201
    assert resposta.data["dados"]["abertura"] == "08:00"
    assert resposta.data["dados"]["fechamento"] == "22:00"


def test_cadastrar_aceita_00_00_como_fechamento_a_meia_noite(cliente_gestor):
    # Act
    resposta = _cadastrar(cliente_gestor, abertura="06:30", fechamento="00:00")

    # Assert
    assert resposta.status_code == 201
    assert resposta.data["dados"]["fechamento"] == "00:00"


def test_horario_aparece_na_listagem_e_no_detalhe(cliente_gestor, cliente_solicitante):
    # Arrange
    criado = _cadastrar(cliente_gestor, abertura="09:00", fechamento="18:30")
    espaco_id = criado.data["dados"]["id"]

    # Act
    listagem = cliente_solicitante.get(URL_LISTA).data["dados"]
    detalhe = cliente_solicitante.get(_detalhe(espaco_id)).data["dados"]

    # Assert
    na_lista = next(espaco for espaco in listagem if espaco["id"] == espaco_id)
    assert (na_lista["abertura"], na_lista["fechamento"]) == ("09:00", "18:30")
    assert (detalhe["abertura"], detalhe["fechamento"]) == ("09:00", "18:30")


def test_campos_antigos_do_espaco_continuam_iguais(cliente_gestor):
    # Act
    dados = _cadastrar(cliente_gestor).data["dados"]

    # Assert
    assert set(dados) >= CAMPOS_DE_SEMPRE
    assert set(dados) == CAMPOS_DE_SEMPRE | {"abertura", "fechamento"}
    assert dados["nome"] == "Ginásio A"
    assert dados["tipo"] == "GINASIO"
    assert dados["tipo_rotulo"] == "Ginásio"
    assert dados["capacidade"] == 50
    assert dados["ativo"] is True


@pytest.mark.parametrize(
    ("corpo", "codigo", "campo"),
    [
        (
            {"abertura": "20:00", "fechamento": "10:00"},
            "HORARIO_DE_FUNCIONAMENTO_INVALIDO",
            "fechamento",
        ),
        (
            {"abertura": "10:00", "fechamento": "10:00"},
            "HORARIO_DE_FUNCIONAMENTO_INVALIDO",
            "fechamento",
        ),
        (
            {"abertura": "10:00", "fechamento": "10:29"},
            "JANELA_DE_FUNCIONAMENTO_CURTA",
            "fechamento",
        ),
    ],
    ids=["fechamento-antes", "fechamento-igual", "janela-de-29-minutos"],
)
def test_cadastrar_com_horario_invalido_responde_400_no_campo(
    cliente_gestor, corpo, codigo, campo
):
    # Act
    resposta = _cadastrar(cliente_gestor, **corpo)

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == codigo
    assert campo in resposta.data["erro"]["campos"]


@pytest.mark.parametrize("campo", ["abertura", "fechamento"])
@pytest.mark.parametrize("valor", ["25:00", "abc", "7h", ""])
def test_horario_fora_do_formato_hora_minuto_responde_400_no_campo(
    cliente_gestor, campo, valor
):
    # Act
    resposta = _cadastrar(cliente_gestor, **{campo: valor})

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "DADOS_INVALIDOS"
    assert campo in resposta.data["erro"]["campos"]


def test_solicitante_nao_cadastra_espaco_com_horario(cliente_solicitante):
    # Act
    resposta = _cadastrar(cliente_solicitante, abertura="08:00", fechamento="22:00")

    # Assert
    assert resposta.status_code == 403


def test_editar_o_horario_mantem_o_resto_do_espaco(cliente_gestor, espaco_id):
    # Act
    resposta = cliente_gestor.patch(
        _detalhe(espaco_id), {"fechamento": "22:00"}, format="json"
    )

    # Assert
    assert resposta.status_code == 200
    dados = resposta.data["dados"]
    assert (dados["abertura"], dados["fechamento"]) == ("07:00", "22:00")
    assert dados["capacidade"] == 20


def test_editar_so_o_horario_nao_e_nenhuma_alteracao_informada(
    cliente_gestor, espaco_id
):
    # Act
    resposta = cliente_gestor.patch(
        _detalhe(espaco_id), {"abertura": "09:00"}, format="json"
    )

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"]["abertura"] == "09:00"


def test_editar_com_horario_invalido_responde_400_e_nao_grava(
    cliente_gestor, espaco_id
):
    # Act
    resposta = cliente_gestor.patch(
        _detalhe(espaco_id), {"abertura": "23:00", "fechamento": "22:00"}, format="json"
    )

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "HORARIO_DE_FUNCIONAMENTO_INVALIDO"
    atual = cliente_gestor.get(_detalhe(espaco_id)).data["dados"]
    assert (atual["abertura"], atual["fechamento"]) == ("07:00", "00:00")


def test_reduzir_o_horario_com_reserva_ativa_fora_da_nova_janela_e_recusado(
    cliente_gestor, cliente_solicitante, espaco_id
):
    # Arrange: reserva Solicitada de 22:30 às 23:30
    assert (
        _solicitar(cliente_solicitante, espaco_id, "22:30", "23:30").status_code == 201
    )

    # Act
    resposta = cliente_gestor.patch(
        _detalhe(espaco_id), {"fechamento": "22:00"}, format="json"
    )

    # Assert
    assert resposta.status_code == 409
    erro = resposta.data["erro"]
    assert erro["codigo"] == "HORARIO_INCOMPATIVEL_COM_RESERVAS"
    assert "1 reserva ativa ficaria fora do novo horário" in erro["mensagem"]
    atual = cliente_gestor.get(_detalhe(espaco_id)).data["dados"]
    assert atual["fechamento"] == "00:00"


def test_reduzir_o_horario_ate_onde_a_reserva_termina_e_aceito(
    cliente_gestor, cliente_solicitante, espaco_id
):
    # Arrange
    assert (
        _solicitar(cliente_solicitante, espaco_id, "22:30", "23:30").status_code == 201
    )

    # Act
    resposta = cliente_gestor.patch(
        _detalhe(espaco_id), {"fechamento": "23:30"}, format="json"
    )

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"]["fechamento"] == "23:30"


def test_reserva_cancelada_nao_impede_reduzir_o_horario(
    cliente_gestor, cliente_solicitante, espaco_id
):
    # Arrange
    reserva_id = _solicitar(cliente_solicitante, espaco_id, "22:30", "23:30").data[
        "dados"
    ]["id"]
    cancelada = cliente_solicitante.patch(
        reverse("reservas:situacao", args=[reserva_id]),
        {"situacao": "CANCELADA", "motivo": "Mudança de planos"},
        format="json",
    )
    assert cancelada.status_code == 200

    # Act
    resposta = cliente_gestor.patch(
        _detalhe(espaco_id), {"fechamento": "22:00"}, format="json"
    )

    # Assert
    assert resposta.status_code == 200


def test_reserva_ate_a_meia_noite_cabe_no_horario_padrao_e_impede_fechar_antes(
    cliente_gestor, cliente_solicitante, espaco_id
):
    # Arrange
    assert (
        _solicitar(cliente_solicitante, espaco_id, "23:00", "00:00").status_code == 201
    )

    # Act
    mais_cedo = cliente_gestor.patch(
        _detalhe(espaco_id), {"fechamento": "23:59"}, format="json"
    )
    ampliando = cliente_gestor.patch(
        _detalhe(espaco_id), {"abertura": "06:00"}, format="json"
    )

    # Assert
    assert mais_cedo.status_code == 409
    assert ampliando.status_code == 200
