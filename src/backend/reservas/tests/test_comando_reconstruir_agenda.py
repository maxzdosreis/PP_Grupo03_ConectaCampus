from datetime import time, timedelta
from io import StringIO

import pytest
from django.core.cache import cache
from django.core.management import CommandError, call_command
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone
from redis.exceptions import RedisError

from reservas.application.ocupacao_do_dia import ocupados_por_reserva
from reservas.application.reconstruir_agenda import ResultadoDaReconstrucao
from reservas.domain.reserva import Reserva
from reservas.infrastructure.agenda_redis import AgendaDoDiaRedis
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango
from reservas.management.commands import reconstruir_agenda_redis
from reservas.tests.fakes import ANA, FUNCIONAMENTO_PADRAO, GESTOR

pytestmark = pytest.mark.django_db

COMANDO = "reconstruir_agenda_redis"
AMANHA = timezone.localdate() + timedelta(days=1)
DEPOIS_DE_AMANHA = AMANHA + timedelta(days=1)


def _executar() -> str:
    saida = StringIO()
    call_command(COMANDO, stdout=saida)
    return saida.getvalue()


def _guardar(espaco_id, data, inicio):
    reserva = Reserva.solicitar(
        espaco_id=espaco_id,
        solicitante=ANA,
        data=data,
        hora_inicio=time(inicio, 0),
        hora_fim=time(inicio + 1, 0),
        finalidade="Treino do time",
        agora=timezone.now(),
        funcionamento=FUNCIONAMENTO_PADRAO,
    )
    return RepositorioReservasDjango().salvar(reserva)


def _do_banco(espaco_id, data):
    reservas = RepositorioReservasDjango().listar_que_ocupam_horario(espaco_id, data)
    return tuple(ocupados_por_reserva(reservas).values())


@pytest.fixture
def agenda():
    return AgendaDoDiaRedis()


def test_o_redis_passa_a_ter_exatamente_o_que_o_postgresql_tem(espaco_id, agenda):
    # Arrange
    _guardar(espaco_id, AMANHA, 9)
    _guardar(espaco_id, AMANHA, 14)
    _guardar(espaco_id, DEPOIS_DE_AMANHA, 10)
    assert agenda.listar(espaco_id, AMANHA) is None

    # Act
    saida = _executar()

    # Assert
    assert agenda.listar(espaco_id, AMANHA) == _do_banco(espaco_id, AMANHA)
    assert len(agenda.listar(espaco_id, AMANHA)) == 2
    assert agenda.listar(espaco_id, DEPOIS_DE_AMANHA) == _do_banco(
        espaco_id, DEPOIS_DE_AMANHA
    )
    assert saida == "Agenda reconstruída: 2 dias, 3 reservas, 0 dias esvaziados.\n"


def test_a_leitura_da_ocupacao_nao_consulta_a_tabela_de_reservas_depois_do_comando(
    espaco_id, cliente_solicitante
):
    # Arrange
    _guardar(espaco_id, AMANHA, 10)
    _executar()

    # Act
    with CaptureQueriesContext(connection) as consultas:
        resposta = cliente_solicitante.get(
            reverse("reservas:ocupacao"),
            {"espaco": espaco_id, "data": AMANHA.isoformat()},
        )

    # Assert
    assert resposta.status_code == 200
    assert len(resposta.data["dados"]["ocupados"]) == 1
    assert not [c for c in consultas if "reservas_reserva" in c["sql"]]


def test_rodar_duas_vezes_da_a_mesma_saida_e_o_mesmo_estado(espaco_id, agenda):
    # Arrange
    _guardar(espaco_id, AMANHA, 10)
    primeira = _executar()
    estado = agenda.listar(espaco_id, AMANHA)

    # Act
    segunda = _executar()

    # Assert
    assert segunda == primeira
    assert agenda.listar(espaco_id, AMANHA) == estado


def test_dia_com_projecao_velha_e_sem_reserva_ativa_e_esvaziado(espaco_id, agenda):
    # Arrange
    reserva = _guardar(espaco_id, AMANHA, 10)
    _executar()
    reserva.alterar_situacao(
        "CANCELADA",
        motivo="Chuva",
        ator=GESTOR,
        agora=timezone.now(),
    )
    RepositorioReservasDjango().salvar(reserva)

    # Act
    saida = _executar()

    # Assert
    assert agenda.listar(espaco_id, AMANHA) == ()
    assert saida == "Agenda reconstruída: 1 dia, 0 reservas, 1 dia esvaziado.\n"


def test_sem_nada_para_refazer_a_saida_diz_zero(espaco_id):
    assert (
        _executar() == "Agenda reconstruída: 0 dias, 0 reservas, 0 dias esvaziados.\n"
    )


@pytest.mark.parametrize(
    ("resultado", "linhas"),
    [
        (
            ResultadoDaReconstrucao(1, 1, 0, 0),
            ["Agenda reconstruída: 1 dia, 1 reserva, 0 dias esvaziados."],
        ),
        (
            ResultadoDaReconstrucao(4, 9, 1, 2),
            [
                "Agenda reconstruída: 4 dias, 9 reservas, 1 dia esvaziado.",
                "2 dias foram descartados porque as reservas mudaram durante a "
                "reconstrução; rode o comando de novo.",
            ],
        ),
        (
            ResultadoDaReconstrucao(0, 0, 0, 1),
            [
                "Agenda reconstruída: 0 dias, 0 reservas, 0 dias esvaziados.",
                "1 dia foi descartado porque as reservas mudaram durante a "
                "reconstrução; rode o comando de novo.",
            ],
        ),
    ],
)
def test_texto_da_saida_no_singular_no_plural_e_com_aviso(
    monkeypatch, resultado, linhas
):
    class CasoDeUsoFixo:
        def executar(self):
            return resultado

    monkeypatch.setattr(
        reconstruir_agenda_redis, "reconstruir_agenda", lambda: CasoDeUsoFixo()
    )

    assert _executar().splitlines() == linhas


def test_redis_fora_do_ar_vira_command_error_com_mensagem_clara(monkeypatch):
    # Arrange
    def falhar(*args, **kwargs):
        raise RedisError("fora do ar")

    monkeypatch.setattr(cache._cache, "get_client", falhar)

    # Act / Assert
    with pytest.raises(CommandError, match="Redis ficou indisponível") as erro:
        _executar()
    assert "rode o comando de novo quando ele voltar" in str(erro.value)


def test_nao_exige_debug(settings, espaco_id):
    settings.DEBUG = False

    assert _executar().startswith("Agenda reconstruída:")
