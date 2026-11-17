import threading
from datetime import datetime, time, timedelta

import pytest
from django.db import connection
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from reservas.domain.intervalo_de_horario import FUSO_HORARIO
from reservas.infrastructure.models import RegistroDeSituacaoModel, ReservaModel

pytestmark = pytest.mark.django_db(transaction=True)

URL_RESERVAS = reverse("reservas:lista")
MOTIVO = "Chuva forte"
MICROSSEGUNDO = timedelta(microseconds=1)


def _dia():
    return timezone.localdate() + timedelta(days=1)


def _inicio():
    return datetime.combine(_dia(), time(10, 0), FUSO_HORARIO)


def _termino():
    return datetime.combine(_dia(), time(11, 0), FUSO_HORARIO)


def _solicitar(cliente, espaco_id):
    resposta = cliente.post(
        URL_RESERVAS,
        {
            "espaco_id": espaco_id,
            "data": _dia().isoformat(),
            "hora_inicio": "10:00",
            "hora_fim": "11:00",
            "finalidade": "Treino",
        },
        format="json",
    )
    return resposta.data["dados"]["id"]


def _alterar(cliente, reserva_id, corpo):
    return cliente.patch(
        reverse("reservas:situacao", args=[reserva_id]), corpo, format="json"
    )


def _historico(cliente, reserva_id):
    return cliente.get(reverse("reservas:historico", args=[reserva_id]))


def _em_outra_conexao(consulta):
    resultado = {}

    def executar():
        try:
            resultado["valor"] = consulta()
        finally:
            connection.close()

    thread = threading.Thread(target=executar)
    thread.start()
    thread.join(timeout=10)
    assert "valor" in resultado, "a leitura em outra conexão não terminou"
    return resultado["valor"]


def _registros_gravados(reserva_id):
    def consulta():
        return list(
            RegistroDeSituacaoModel.objects.filter(reserva_id=reserva_id).order_by(
                "registrado_em", "id"
            )
        )

    return _em_outra_conexao(consulta)


def _tentativas_gravadas(reserva_id):
    return [r for r in _registros_gravados(reserva_id) if r.resultado == "RECUSADA"]


def _situacao_gravada(reserva_id):
    return _em_outra_conexao(
        lambda: ReservaModel.objects.values_list("situacao", flat=True).get(
            pk=reserva_id
        )
    )


def _total_de_registros():
    return _em_outra_conexao(RegistroDeSituacaoModel.objects.count)


@pytest.fixture
def reserva_id(cliente_solicitante, espaco_id):
    return _solicitar(cliente_solicitante, espaco_id)


@pytest.fixture
def confirmada_id(cliente_gestor, reserva_id):
    assert (
        _alterar(cliente_gestor, reserva_id, {"situacao": "CONFIRMADA"}).status_code
        == 200
    )
    return reserva_id


def _conferir_tentativa(tentativa, *, autor, pedida, codigo, momento, situacao):
    assert tentativa.resultado == "RECUSADA"
    assert tentativa.autor_nome == autor
    assert tentativa.situacao_pedida == pedida
    assert tentativa.codigo_do_erro == codigo
    assert tentativa.registrado_em == momento
    assert tentativa.situacao_anterior == tentativa.situacao_nova == situacao


def test_gestor_concluindo_antes_do_termino_e_recusado_mas_a_tentativa_fica_gravada(
    cliente_gestor, confirmada_id, relogio_da_api
):
    # Arrange
    momento = _termino() - MICROSSEGUNDO
    relogio_da_api(momento)

    # Act
    resposta = _alterar(cliente_gestor, confirmada_id, {"situacao": "CONCLUIDA"})

    # Assert
    assert resposta.status_code == 409
    assert resposta.data["erro"]["codigo"] == "CONCLUSAO_ANTES_DO_TERMINO"
    assert _situacao_gravada(confirmada_id) == "CONFIRMADA"
    (tentativa,) = _tentativas_gravadas(confirmada_id)
    _conferir_tentativa(
        tentativa,
        autor="Gestora de Teste",
        pedida="CONCLUIDA",
        codigo="CONCLUSAO_ANTES_DO_TERMINO",
        momento=momento,
        situacao="CONFIRMADA",
    )


def test_gestor_recusando_depois_do_inicio_e_recusado_mas_a_tentativa_fica_gravada(
    cliente_gestor, reserva_id, relogio_da_api
):
    # Arrange
    relogio_da_api(_inicio())

    # Act
    resposta = _alterar(
        cliente_gestor, reserva_id, {"situacao": "RECUSADA", "motivo": MOTIVO}
    )

    # Assert
    assert resposta.status_code == 409
    assert resposta.data["erro"]["codigo"] == "RECUSA_OU_CANCELAMENTO_APOS_O_INICIO"
    assert _situacao_gravada(reserva_id) == "SOLICITADA"
    (tentativa,) = _tentativas_gravadas(reserva_id)
    _conferir_tentativa(
        tentativa,
        autor="Gestora de Teste",
        pedida="RECUSADA",
        codigo="RECUSA_OU_CANCELAMENTO_APOS_O_INICIO",
        momento=_inicio(),
        situacao="SOLICITADA",
    )
    assert tentativa.motivo == MOTIVO


def test_solicitante_confirmando_e_recusado_mas_a_tentativa_fica_gravada(
    cliente_solicitante, reserva_id, relogio_da_api
):
    # Arrange
    momento = timezone.now()
    relogio_da_api(momento)

    # Act
    resposta = _alterar(cliente_solicitante, reserva_id, {"situacao": "CONFIRMADA"})

    # Assert
    assert resposta.status_code == 403
    assert resposta.data["erro"]["codigo"] == "ACAO_NAO_PERMITIDA"
    assert _situacao_gravada(reserva_id) == "SOLICITADA"
    (tentativa,) = _tentativas_gravadas(reserva_id)
    _conferir_tentativa(
        tentativa,
        autor="Ana Souza",
        pedida="CONFIRMADA",
        codigo="ACAO_NAO_PERMITIDA",
        momento=momento,
        situacao="SOLICITADA",
    )


def test_transicao_invalida_e_recusada_mas_a_tentativa_fica_gravada(
    cliente_gestor, reserva_id, relogio_da_api
):
    # Arrange
    _alterar(cliente_gestor, reserva_id, {"situacao": "RECUSADA", "motivo": MOTIVO})
    momento = timezone.now()
    relogio_da_api(momento)

    # Act
    resposta = _alterar(cliente_gestor, reserva_id, {"situacao": "CONCLUIDA"})

    # Assert
    assert resposta.status_code == 409
    assert resposta.data["erro"]["codigo"] == "TRANSICAO_DE_SITUACAO_INVALIDA"
    assert _situacao_gravada(reserva_id) == "RECUSADA"
    (tentativa,) = _tentativas_gravadas(reserva_id)
    _conferir_tentativa(
        tentativa,
        autor="Gestora de Teste",
        pedida="CONCLUIDA",
        codigo="TRANSICAO_DE_SITUACAO_INVALIDA",
        momento=momento,
        situacao="RECUSADA",
    )


def test_motivo_ausente_e_recusado_mas_a_tentativa_fica_gravada(
    cliente_gestor, reserva_id
):
    # Act
    resposta = _alterar(cliente_gestor, reserva_id, {"situacao": "CANCELADA"})

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "MOTIVO_OBRIGATORIO"
    (tentativa,) = _tentativas_gravadas(reserva_id)
    assert tentativa.codigo_do_erro == "MOTIVO_OBRIGATORIO"
    assert tentativa.situacao_pedida == "CANCELADA"
    assert _situacao_gravada(reserva_id) == "SOLICITADA"


def test_situacao_desconhecida_e_recusada_e_o_texto_pedido_fica_gravado(
    cliente_gestor, reserva_id
):
    # Act
    resposta = _alterar(cliente_gestor, reserva_id, {"situacao": "  em  análise "})

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "SITUACAO_INVALIDA"
    (tentativa,) = _tentativas_gravadas(reserva_id)
    assert tentativa.situacao_pedida == "em análise"
    assert tentativa.codigo_do_erro == "SITUACAO_INVALIDA"
    registro = _historico(cliente_gestor, reserva_id).data["dados"][-1]
    assert registro["situacao_pedida_rotulo"] is None


def test_cada_recusa_grava_exatamente_um_registro(cliente_gestor, reserva_id):
    # Arrange
    antes = len(_registros_gravados(reserva_id))

    # Act
    _alterar(cliente_gestor, reserva_id, {"situacao": "CANCELADA"})

    # Assert
    assert len(_registros_gravados(reserva_id)) == antes + 1


def test_gestor_cancelando_concluida_e_recusado_e_a_tentativa_aparece_no_historico(
    cliente_gestor, confirmada_id, relogio_da_api
):
    # Arrange
    relogio_da_api(_termino())
    assert (
        _alterar(cliente_gestor, confirmada_id, {"situacao": "CONCLUIDA"}).status_code
        == 200
    )

    # Act
    resposta = _alterar(
        cliente_gestor, confirmada_id, {"situacao": "CANCELADA", "motivo": MOTIVO}
    )

    # Assert
    assert resposta.status_code == 409
    assert resposta.data["erro"]["codigo"] == "TRANSICAO_DE_SITUACAO_INVALIDA"
    assert _situacao_gravada(confirmada_id) == "CONCLUIDA"
    historico = _historico(cliente_gestor, confirmada_id).data["dados"]
    assert historico[-1]["resultado"] == "RECUSADA"
    assert historico[-1]["situacao_pedida"] == "CANCELADA"
    assert historico[-1]["codigo_do_erro"] == "TRANSICAO_DE_SITUACAO_INVALIDA"
    assert historico[-1]["situacao_nova"] == "CONCLUIDA"


def test_tentativa_depois_da_confirmacao_aparece_distinta_da_mudanca_aceita(
    cliente_gestor, confirmada_id, relogio_da_api
):
    # Arrange
    relogio_da_api(_termino() - MICROSSEGUNDO)
    _alterar(cliente_gestor, confirmada_id, {"situacao": "CONCLUIDA"})

    # Act
    registros = _historico(cliente_gestor, confirmada_id).data["dados"]

    # Assert
    assert [(r["resultado"], r["situacao_pedida"]) for r in registros] == [
        ("ACEITA", "SOLICITADA"),
        ("ACEITA", "CONFIRMADA"),
        ("RECUSADA", "CONCLUIDA"),
    ]
    assert _situacao_gravada(confirmada_id) == "CONFIRMADA"


def test_solicitante_que_nao_e_dono_recebe_404_e_nada_e_registrado(
    outro_solicitante, reserva_id
):
    # Arrange
    cliente = APIClient()
    cliente.force_authenticate(user=outro_solicitante)
    antes = _total_de_registros()

    # Act
    resposta = _alterar(
        cliente, reserva_id, {"situacao": "CANCELADA", "motivo": MOTIVO}
    )

    # Assert
    assert resposta.status_code == 404
    assert resposta.data["erro"]["codigo"] == "RESERVA_NAO_ENCONTRADA"
    assert _total_de_registros() == antes
    assert _historico(cliente, reserva_id).status_code == 404


def test_anonimo_recebe_401_e_nada_e_registrado(reserva_id):
    # Arrange
    antes = _total_de_registros()

    # Act
    resposta = _alterar(APIClient(), reserva_id, {"situacao": "CANCELADA"})

    # Assert
    assert resposta.status_code == 401
    assert _total_de_registros() == antes


def test_reserva_inexistente_recebe_404_e_nada_e_registrado(cliente_gestor):
    # Act
    resposta = _alterar(cliente_gestor, 9999, {"situacao": "CONFIRMADA"})

    # Assert
    assert resposta.status_code == 404
    assert _total_de_registros() == 0


@pytest.mark.parametrize(
    "corpo", [{}, {"situacao": ""}, {"situacao": "   "}, {"motivo": "x"}]
)
def test_pedido_sem_situacao_e_erro_de_formato_e_nada_e_registrado(
    cliente_gestor, reserva_id, corpo
):
    # Arrange
    antes = _total_de_registros()

    # Act
    resposta = _alterar(cliente_gestor, reserva_id, corpo)

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "DADOS_INVALIDOS"
    assert _total_de_registros() == antes


def test_mudanca_aceita_nao_gera_tentativa(cliente_gestor, reserva_id):
    # Act
    resposta = _alterar(cliente_gestor, reserva_id, {"situacao": "CONFIRMADA"})

    # Assert
    assert resposta.status_code == 200
    assert _tentativas_gravadas(reserva_id) == []


def _gerar_tentativas(cliente_solicitante, cliente_gestor, reserva_id, relogio_da_api):
    agora = timezone.now()
    relogio_da_api(agora + timedelta(minutes=1))
    _alterar(cliente_solicitante, reserva_id, {"situacao": "CONFIRMADA"})
    relogio_da_api(agora + timedelta(minutes=2))
    _alterar(cliente_gestor, reserva_id, {"situacao": "CONFIRMADA"})
    relogio_da_api(agora + timedelta(minutes=3))
    _alterar(cliente_gestor, reserva_id, {"situacao": "CONCLUIDA"})


def test_historico_mistura_aceitas_e_recusadas_em_ordem_cronologica(
    cliente_solicitante, cliente_gestor, reserva_id, relogio_da_api
):
    # Arrange
    _gerar_tentativas(cliente_solicitante, cliente_gestor, reserva_id, relogio_da_api)

    # Act
    registros = _historico(cliente_gestor, reserva_id).data["dados"]

    # Assert
    assert [(r["resultado"], r["situacao_pedida"]) for r in registros] == [
        ("ACEITA", "SOLICITADA"),
        ("RECUSADA", "CONFIRMADA"),
        ("ACEITA", "CONFIRMADA"),
        ("RECUSADA", "CONCLUIDA"),
    ]
    momentos = [r["registrado_em"] for r in registros]
    assert momentos == sorted(momentos)


def test_dono_e_gestor_veem_as_mesmas_tentativas(
    cliente_solicitante, cliente_gestor, reserva_id, relogio_da_api
):
    # Arrange
    _gerar_tentativas(cliente_solicitante, cliente_gestor, reserva_id, relogio_da_api)

    # Act
    do_dono = _historico(cliente_solicitante, reserva_id).data["dados"]
    do_gestor = _historico(cliente_gestor, reserva_id).data["dados"]

    # Assert
    assert do_dono == do_gestor
    autores = [r["autor"]["nome"] for r in do_dono if r["resultado"] == "RECUSADA"]
    assert autores == ["Ana Souza", "Gestora de Teste"]


def test_outro_solicitante_nao_ve_as_tentativas_de_uma_reserva_alheia(
    cliente_solicitante, cliente_gestor, outro_solicitante, reserva_id, relogio_da_api
):
    # Arrange
    _gerar_tentativas(cliente_solicitante, cliente_gestor, reserva_id, relogio_da_api)
    cliente = APIClient()
    cliente.force_authenticate(user=outro_solicitante)

    # Act
    resposta = _historico(cliente, reserva_id)

    # Assert
    assert resposta.status_code == 404
    assert "RECUSADA" not in resposta.content.decode()


def test_historico_mantem_os_campos_anteriores_e_acrescenta_os_novos(
    cliente_gestor, reserva_id
):
    # Arrange
    _alterar(cliente_gestor, reserva_id, {"situacao": "CONFIRMADA"})
    _alterar(cliente_gestor, reserva_id, {"situacao": "CANCELADA"})

    # Act
    criacao, aceita, recusada = _historico(cliente_gestor, reserva_id).data["dados"]

    # Assert
    campos_anteriores = {
        "situacao_anterior",
        "situacao_anterior_rotulo",
        "situacao_nova",
        "situacao_nova_rotulo",
        "motivo",
        "autor",
        "registrado_em",
    }
    campos_novos = {
        "resultado",
        "situacao_pedida",
        "situacao_pedida_rotulo",
        "codigo_do_erro",
    }
    for registro in (criacao, aceita, recusada):
        assert set(registro) == campos_anteriores | campos_novos
    assert criacao["situacao_anterior"] is None
    assert criacao["situacao_nova"] == "SOLICITADA"
    assert (aceita["situacao_anterior"], aceita["situacao_nova"]) == (
        "SOLICITADA",
        "CONFIRMADA",
    )
    assert aceita["resultado"] == "ACEITA"
    assert aceita["situacao_pedida"] == "CONFIRMADA"
    assert aceita["codigo_do_erro"] is None
    assert recusada["resultado"] == "RECUSADA"
    assert recusada["situacao_pedida"] == "CANCELADA"
    assert recusada["situacao_pedida_rotulo"] == "Cancelada"
    assert recusada["codigo_do_erro"] == "MOTIVO_OBRIGATORIO"
    assert recusada["situacao_nova"] == "CONFIRMADA"
    assert recusada["autor"] == {"nome": "Gestora de Teste"}
