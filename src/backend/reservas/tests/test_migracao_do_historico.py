from datetime import datetime, timedelta

import pytest
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.utils import timezone

ANTES = [("reservas", "0002_registrodesituacaomodel")]
DEPOIS = [("reservas", "0003_tentativas_recusadas_no_historico")]

pytestmark = pytest.mark.django_db(transaction=True)


def _migrar_para(alvo):
    executor = MigrationExecutor(connection)
    executor.migrate(alvo)
    return executor.loader.project_state(alvo).apps


@pytest.fixture
def banco_na_migration_anterior():
    apps = _migrar_para(ANTES)
    yield apps
    executor = MigrationExecutor(connection)
    executor.migrate(executor.loader.graph.leaf_nodes())


def _criar_reserva_com_historico(apps):
    reserva_model = apps.get_model("reservas", "ReservaModel")
    registro_model = apps.get_model("reservas", "RegistroDeSituacaoModel")
    inicio = timezone.now() + timedelta(days=1)
    reserva = reserva_model.objects.create(
        espaco_id=1,
        solicitante_usuario_id=7,
        solicitante_nome="Ana Souza",
        solicitante_matricula="2026001",
        inicio=inicio,
        fim=inicio + timedelta(hours=1),
        finalidade="Treino",
        situacao="CONFIRMADA",
        criada_em=timezone.now(),
    )
    criacao = registro_model.objects.create(
        reserva=reserva,
        situacao_anterior="",
        situacao_nova="SOLICITADA",
        autor_usuario_id=7,
        autor_nome="Ana Souza",
        registrado_em=timezone.now(),
    )
    confirmacao = registro_model.objects.create(
        reserva=reserva,
        situacao_anterior="SOLICITADA",
        situacao_nova="CONFIRMADA",
        autor_usuario_id=1,
        autor_nome="Gestora de Teste",
        registrado_em=timezone.now(),
    )
    return reserva.pk, criacao.pk, confirmacao.pk


def test_registros_antigos_viram_aceitos_e_os_dados_ficam(banco_na_migration_anterior):
    # Arrange
    reserva_id, criacao_id, confirmacao_id = _criar_reserva_com_historico(
        banco_na_migration_anterior
    )

    # Act
    apps = _migrar_para(DEPOIS)

    # Assert
    registro = apps.get_model("reservas", "RegistroDeSituacaoModel")
    criacao = registro.objects.get(pk=criacao_id)
    confirmacao = registro.objects.get(pk=confirmacao_id)
    assert registro.objects.filter(reserva_id=reserva_id).count() == 2
    assert (criacao.resultado, criacao.codigo_do_erro) == ("ACEITA", "")
    assert (criacao.situacao_anterior, criacao.situacao_nova) == ("", "SOLICITADA")
    assert criacao.situacao_pedida == "SOLICITADA"
    assert (confirmacao.resultado, confirmacao.codigo_do_erro) == ("ACEITA", "")
    assert (confirmacao.situacao_anterior, confirmacao.situacao_nova) == (
        "SOLICITADA",
        "CONFIRMADA",
    )
    assert confirmacao.situacao_pedida == "CONFIRMADA"
    assert confirmacao.autor_nome == "Gestora de Teste"


def test_depois_da_migration_o_banco_aceita_uma_tentativa_recusada(
    banco_na_migration_anterior,
):
    # Arrange
    reserva_id, _, _ = _criar_reserva_com_historico(banco_na_migration_anterior)
    apps = _migrar_para(DEPOIS)
    registro = apps.get_model("reservas", "RegistroDeSituacaoModel")

    # Act
    tentativa = registro.objects.create(
        reserva_id=reserva_id,
        situacao_anterior="CONFIRMADA",
        situacao_nova="CONFIRMADA",
        autor_usuario_id=7,
        autor_nome="Ana Souza",
        registrado_em=datetime.now(tz=timezone.get_current_timezone()),
        resultado="RECUSADA",
        codigo_do_erro="ACAO_NAO_PERMITIDA",
        situacao_pedida="CONCLUIDA",
    )

    # Assert
    assert registro.objects.get(pk=tentativa.pk).resultado == "RECUSADA"


def test_a_migration_e_reversivel_e_descarta_so_as_tentativas(
    banco_na_migration_anterior,
):
    # Arrange
    reserva_id, _, _ = _criar_reserva_com_historico(banco_na_migration_anterior)
    apps = _migrar_para(DEPOIS)
    apps.get_model("reservas", "RegistroDeSituacaoModel").objects.create(
        reserva_id=reserva_id,
        situacao_anterior="CONFIRMADA",
        situacao_nova="CONFIRMADA",
        autor_usuario_id=7,
        autor_nome="Ana Souza",
        registrado_em=timezone.now(),
        resultado="RECUSADA",
        codigo_do_erro="ACAO_NAO_PERMITIDA",
        situacao_pedida="CONCLUIDA",
    )

    # Act
    apps_antigos = _migrar_para(ANTES)

    # Assert
    registro = apps_antigos.get_model("reservas", "RegistroDeSituacaoModel")
    assert registro.objects.filter(reserva_id=reserva_id).count() == 2
    with connection.cursor() as cursor:
        colunas = {
            c.name
            for c in connection.introspection.get_table_description(
                cursor, "reservas_registro_de_situacao"
            )
        }
    assert {"resultado", "codigo_do_erro", "situacao_pedida"}.isdisjoint(colunas)
