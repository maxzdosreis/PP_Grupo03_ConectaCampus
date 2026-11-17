from datetime import datetime, time
from zoneinfo import ZoneInfo

import pytest
from django.apps import apps
from django.db import connection
from django.db.migrations.executor import MigrationExecutor

from espacos.domain.horario_de_funcionamento import HorarioDeFuncionamento
from espacos.infrastructure.repositorio_django import RepositorioEspacosDjango

FUSO_HORARIO = ZoneInfo("America/Sao_Paulo")

ANTES = [("espacos", "0001_initial")]
DEPOIS = [("espacos", "0002_horario_de_funcionamento")]

pytestmark = pytest.mark.django_db(transaction=True)


def _migrar(destino):
    executor = MigrationExecutor(connection)
    executor.migrate(destino)
    return MigrationExecutor(connection)


@pytest.fixture
def banco_antes_da_migracao():
    """Leva o banco ao estado anterior ao horário e o devolve ao final do teste."""
    executor = _migrar(ANTES)
    yield executor.loader.project_state(ANTES).apps
    _migrar(MigrationExecutor(connection).loader.graph.leaf_nodes())


def _reserva_antiga(espaco_id, inicio, fim):
    dia = datetime(2026, 11, 20)
    return apps.get_model("reservas", "ReservaModel").objects.create(
        espaco_id=espaco_id,
        solicitante_usuario_id=7,
        solicitante_nome="Ana Souza",
        solicitante_matricula="2026001",
        inicio=datetime.combine(dia, inicio, tzinfo=FUSO_HORARIO),
        fim=datetime.combine(dia, fim, tzinfo=FUSO_HORARIO),
        finalidade="Treino do time de vôlei",
        situacao="CONFIRMADA",
        motivo_da_situacao="",
        criada_em=datetime(2026, 11, 1, 12, 0, tzinfo=FUSO_HORARIO),
    )


def test_espacos_existentes_recebem_o_horario_padrao_e_os_dados_ficam(
    banco_antes_da_migracao,
):
    # Arrange
    modelo_antigo = banco_antes_da_migracao.get_model("espacos", "EspacoEsportivoModel")
    antigo = modelo_antigo.objects.create(
        nome="Ginásio Antigo", tipo="GINASIO", capacidade=40, ativo=True
    )
    inativo = modelo_antigo.objects.create(
        nome="Quadra Velha", tipo="QUADRA_DE_AREIA", capacidade=8, ativo=False
    )

    # Act
    _migrar(DEPOIS)

    # Assert
    repositorio = RepositorioEspacosDjango()
    for espaco_id, nome, capacidade, ativo in [
        (antigo.pk, "Ginásio Antigo", 40, True),
        (inativo.pk, "Quadra Velha", 8, False),
    ]:
        espaco = repositorio.obter_por_id(espaco_id)
        assert (espaco.nome, espaco.capacidade, espaco.ativo) == (
            nome,
            capacidade,
            ativo,
        )
        assert espaco.horario == HorarioDeFuncionamento.padrao()
        assert (espaco.horario.abertura(), espaco.horario.fechamento()) == (
            time(7, 0),
            time(0, 0),
        )


def test_reservas_antigas_continuam_dentro_do_horario_do_espaco_depois_da_migracao(
    banco_antes_da_migracao,
):
    # Arrange
    modelo_antigo = banco_antes_da_migracao.get_model("espacos", "EspacoEsportivoModel")
    espaco_id = modelo_antigo.objects.create(
        nome="Ginásio Antigo", tipo="GINASIO", capacidade=40
    ).pk
    na_abertura = _reserva_antiga(espaco_id, time(7, 0), time(8, 0))
    no_antigo_fechamento = _reserva_antiga(espaco_id, time(21, 0), time(22, 0))

    # Act
    _migrar(DEPOIS)

    # Assert
    horario = RepositorioEspacosDjango().obter_por_id(espaco_id).horario
    for modelo in (na_abertura, no_antigo_fechamento):
        modelo.refresh_from_db()
        inicio = modelo.inicio.astimezone(FUSO_HORARIO)
        fim = modelo.fim.astimezone(FUSO_HORARIO)
        inicio_em_minutos = inicio.hour * 60 + inicio.minute
        fim_em_minutos = fim.hour * 60 + fim.minute
        assert horario.abertura_em_minutos <= inicio_em_minutos
        assert fim_em_minutos <= horario.fechamento_em_minutos
        assert modelo.situacao == "CONFIRMADA"


def test_a_migracao_pode_ser_desfeita_sem_perder_os_dados_do_espaco(
    banco_antes_da_migracao,
):
    # Arrange
    modelo_antigo = banco_antes_da_migracao.get_model("espacos", "EspacoEsportivoModel")
    espaco_id = modelo_antigo.objects.create(
        nome="Ginásio Antigo", tipo="GINASIO", capacidade=40
    ).pk
    _migrar(DEPOIS)

    # Act
    apps = _migrar(ANTES).loader.project_state(ANTES).apps

    # Assert
    voltou = apps.get_model("espacos", "EspacoEsportivoModel").objects.get(pk=espaco_id)
    assert (voltou.nome, voltou.capacidade) == ("Ginásio Antigo", 40)
    assert not hasattr(voltou, "abertura_em_minutos")
