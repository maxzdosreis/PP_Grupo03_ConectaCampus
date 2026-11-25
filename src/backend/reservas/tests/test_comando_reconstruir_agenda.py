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
from reservas.application.portas import IndiceIndisponivel
from reservas.application.reconstruir_agenda import ResultadoDaReconstrucao
from reservas.application.reconstruir_indice import ResultadoDaReconstrucaoDoIndice
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.agenda_redis import AgendaDoDiaRedis
from reservas.infrastructure.indice_redis import IndiceDeReservasRedis
from reservas.infrastructure.models import ReservaModel
from reservas.infrastructure.repositorio_com_agenda import RepositorioReservasComAgenda
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


def _da_agenda(saida: str) -> str:
    linhas = [
        linha
        for linha in saida.splitlines(keepends=True)
        if "Filas e contagens" not in linha
    ]
    return "".join(linhas)


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
    saida = _da_agenda(_executar())

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
    saida = _da_agenda(_executar())

    # Assert
    assert agenda.listar(espaco_id, AMANHA) == ()
    assert saida == "Agenda reconstruída: 1 dia, 0 reservas, 1 dia esvaziado.\n"


def test_sem_nada_para_refazer_a_saida_diz_zero(espaco_id):
    assert _da_agenda(_executar()) == (
        "Agenda reconstruída: 0 dias, 0 reservas, 0 dias esvaziados.\n"
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

    assert _da_agenda(_executar()).splitlines() == linhas


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


def _linha_do_indice(saida: str) -> str:
    [linha] = [x for x in saida.splitlines() if "Filas e contagens" in x]
    return linha


def _salvar_na_situacao(espaco_id, inicio, situacao):
    reserva = Reserva.solicitar(
        espaco_id=espaco_id,
        solicitante=ANA,
        data=AMANHA,
        hora_inicio=time(inicio, 0),
        hora_fim=time(inicio + 1, 0),
        finalidade="Treino do time",
        agora=timezone.now(),
        funcionamento=FUNCIONAMENTO_PADRAO,
    )
    if situacao is not SituacaoReserva.SOLICITADA:
        reserva.alterar_situacao(
            situacao,
            motivo="Chuva" if situacao is SituacaoReserva.CANCELADA else None,
            ator=GESTOR,
            agora=timezone.now(),
        )
    return RepositorioReservasDjango().salvar(reserva)


def _estado_do_postgresql() -> tuple[tuple[int, ...], dict]:
    do_banco = ReservaModel.objects.order_by("criada_em", "id")
    fila = tuple(
        m.id for m in do_banco if m.situacao == SituacaoReserva.SOLICITADA.value
    )
    contagem = {
        situacao: ReservaModel.objects.filter(situacao=situacao.value).count()
        for situacao in SituacaoReserva
    }
    return fila, contagem


@pytest.fixture
def indice():
    return IndiceDeReservasRedis()


def test_o_redis_passa_a_ter_fila_e_conjuntos_iguais_ao_postgresql(espaco_id, indice):
    # Arrange
    _salvar_na_situacao(espaco_id, 8, SituacaoReserva.SOLICITADA)
    _salvar_na_situacao(espaco_id, 9, SituacaoReserva.CONFIRMADA)
    _salvar_na_situacao(espaco_id, 10, SituacaoReserva.SOLICITADA)
    _salvar_na_situacao(espaco_id, 11, SituacaoReserva.CANCELADA)
    assert indice.pendentes(10) is None

    # Act
    saida = _executar()

    # Assert
    fila, contagem = _estado_do_postgresql()
    assert indice.pendentes(100) == fila
    assert len(fila) == 2
    assert indice.contagem_por_situacao() == contagem
    assert _linha_do_indice(saida) == (
        "Filas e contagens reconstruídas: 4 reservas, 2 pendentes."
    )


def test_a_segunda_linha_vem_depois_da_linha_da_agenda_que_fica_intacta(espaco_id):
    # Arrange
    _salvar_na_situacao(espaco_id, 8, SituacaoReserva.SOLICITADA)

    # Act
    linhas = _executar().splitlines()

    # Assert
    assert linhas == [
        "Agenda reconstruída: 1 dia, 1 reserva, 0 dias esvaziados.",
        "Filas e contagens reconstruídas: 1 reserva, 1 pendente.",
    ]


def test_sem_reservas_o_indice_fica_montado_e_vazio(indice):
    # Act
    saida = _executar()

    # Assert
    assert indice.pendentes(10) == ()
    assert indice.contagem_por_situacao() == dict.fromkeys(SituacaoReserva, 0)
    assert _linha_do_indice(saida) == (
        "Filas e contagens reconstruídas: 0 reservas, 0 pendentes."
    )


def test_rodar_duas_vezes_da_a_mesma_saida_e_o_mesmo_estado_do_indice(
    espaco_id, indice
):
    # Arrange
    _salvar_na_situacao(espaco_id, 8, SituacaoReserva.SOLICITADA)
    _salvar_na_situacao(espaco_id, 9, SituacaoReserva.CONFIRMADA)
    primeira = _executar()
    estado = (indice.pendentes(10), indice.contagem_por_situacao())

    # Act
    segunda = _executar()

    # Assert
    assert segunda == primeira
    assert (indice.pendentes(10), indice.contagem_por_situacao()) == estado


def test_decorator_apos_a_reconstrucao_atualiza_fila_e_contagens(espaco_id, indice):
    # Arrange
    _executar()
    repositorio = RepositorioReservasComAgenda(
        RepositorioReservasDjango(),
        AgendaDoDiaRedis(),
        indice,
        apos_o_commit=lambda acao: acao(),
    )
    reserva = Reserva.solicitar(
        espaco_id=espaco_id,
        solicitante=ANA,
        data=AMANHA,
        hora_inicio=time(14, 0),
        hora_fim=time(15, 0),
        finalidade="Treino do time",
        agora=timezone.now(),
        funcionamento=FUNCIONAMENTO_PADRAO,
    )

    # Act e Assert: criar
    salva = repositorio.salvar(reserva)
    assert indice.pendentes(10) == (salva.id,)
    assert indice.contagem_por_situacao()[SituacaoReserva.SOLICITADA] == 1

    # Act e Assert: mudar a situação
    salva.alterar_situacao(
        SituacaoReserva.CONFIRMADA, ator=GESTOR, agora=timezone.now()
    )
    repositorio.salvar(salva)
    assert indice.pendentes(10) == ()
    assert indice.contagem_por_situacao() == _estado_do_postgresql()[1]


@pytest.mark.parametrize(
    ("resultado", "esperada"),
    [
        (
            ResultadoDaReconstrucaoDoIndice(1, 1, False),
            "Filas e contagens reconstruídas: 1 reserva, 1 pendente.",
        ),
        (
            ResultadoDaReconstrucaoDoIndice(9, 3, False),
            "Filas e contagens reconstruídas: 9 reservas, 3 pendentes.",
        ),
        (
            ResultadoDaReconstrucaoDoIndice(0, 0, True),
            "As filas e contagens foram descartadas porque as reservas mudaram "
            "durante a reconstrução; rode o comando de novo.",
        ),
    ],
)
def test_texto_da_linha_do_indice_no_singular_no_plural_e_com_aviso(
    monkeypatch, resultado, esperada
):
    class CasoDeUsoFixo:
        def executar(self):
            return resultado

    monkeypatch.setattr(
        reconstruir_agenda_redis, "reconstruir_indice", lambda: CasoDeUsoFixo()
    )

    assert _executar().splitlines()[1:] == [esperada]


def test_indice_descartado_aparece_como_aviso_e_nao_como_sucesso(monkeypatch):
    # Arrange
    class CasoDeUsoFixo:
        def executar(self):
            return ResultadoDaReconstrucaoDoIndice(0, 0, True)

    monkeypatch.setattr(
        reconstruir_agenda_redis, "reconstruir_indice", lambda: CasoDeUsoFixo()
    )

    # Act e Assert
    assert "Filas e contagens reconstruídas" not in _executar()


def test_indice_fora_do_ar_depois_da_agenda_vira_command_error_que_diz_isso(
    monkeypatch,
):
    # Arrange
    class CasoDeUsoQueFalha:
        def executar(self):
            raise IndiceIndisponivel

    monkeypatch.setattr(
        reconstruir_agenda_redis, "reconstruir_indice", lambda: CasoDeUsoQueFalha()
    )

    # Act e Assert
    with pytest.raises(CommandError, match="agenda foi reconstruída") as erro:
        _executar()
    assert "filas e contagens" in str(erro.value)
    assert "rode o comando de novo quando ele voltar" in str(erro.value)


def test_agenda_fora_do_ar_nem_chega_a_tentar_o_indice(monkeypatch):
    # Arrange
    def nao_deveria_ser_chamado():
        raise AssertionError("o índice não deveria ser reconstruído")

    def falhar(*args, **kwargs):
        raise RedisError("fora do ar")

    monkeypatch.setattr(cache._cache, "get_client", falhar)
    monkeypatch.setattr(
        reconstruir_agenda_redis, "reconstruir_indice", nao_deveria_ser_chamado
    )

    # Act e Assert
    with pytest.raises(CommandError, match="reconstrução da agenda"):
        _executar()


def test_a_ajuda_do_comando_fala_da_agenda_e_das_filas_e_contagens():
    ajuda = reconstruir_agenda_redis.Command.help

    assert "agenda" in ajuda
    assert "filas e contagens" in ajuda
