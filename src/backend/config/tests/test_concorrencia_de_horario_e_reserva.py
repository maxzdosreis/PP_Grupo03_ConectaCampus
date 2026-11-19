import threading
import time
from datetime import time as hora
from datetime import timedelta
from zoneinfo import ZoneInfo

import pytest
from django.db import connection
from django.utils import timezone

from espacos.application.casos_de_uso import EditarEspaco
from espacos.domain.excecoes import HorarioIncompativelComReservas
from espacos.infrastructure.models import EspacoEsportivoModel
from espacos.infrastructure.repositorio_django import RepositorioEspacosDjango
from espacos.tests.fakes import novo_espaco
from reservas.api.dependencias import ReservasDoEspacoViaCasoDeUso, criar_reserva
from reservas.application.casos_de_uso import CriarReserva
from reservas.domain.excecoes import ForaDoHorarioDeFuncionamento
from reservas.infrastructure.consulta_de_espacos import ConsultaDeEspacosViaFachada
from reservas.infrastructure.models import ReservaModel
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango
from reservas.tests.fakes import ANA

ESPERA_MAXIMA_S = 10
FUSO = ZoneInfo("America/Sao_Paulo")


class _Sinais:
    def __init__(self) -> None:
        self.pausada = threading.Event()
        self.liberar = threading.Event()

    def pausar(self) -> None:
        self.pausada.set()
        assert self.liberar.wait(ESPERA_MAXIMA_S), "ninguém liberou a thread pausada"


class _ContagemPausada(ReservasDoEspacoViaCasoDeUso):
    """Pausa a edição logo depois de contar as reservas fora da nova janela."""

    def __init__(self, sinais: _Sinais) -> None:
        self._sinais = sinais

    def contar_ativas_fora_da_janela(self, *argumentos) -> int:
        fora = super().contar_ativas_fora_da_janela(*argumentos)
        self._sinais.pausar()
        return fora


class _LeituraDoEspacoPausada(ConsultaDeEspacosViaFachada):
    def __init__(self, sinais: _Sinais) -> None:
        self._sinais = sinais

    def obter_espaco_reservavel_travado(self, espaco_id: int):
        espaco = super().obter_espaco_reservavel_travado(espaco_id)
        self._sinais.pausar()
        return espaco


def _em_thread(resultados: dict, nome: str, acao) -> threading.Thread:
    def executar() -> None:
        try:
            with connection.cursor() as cursor:
                cursor.execute("SET statement_timeout = 8000; SET lock_timeout = 8000")
            resultados[nome] = acao()
        except Exception as erro:
            resultados[nome] = erro
        finally:
            connection.close()

    thread = threading.Thread(target=executar)
    thread.start()
    return thread


def _esperar_alguem_esperando_uma_trava() -> None:
    limite = time.monotonic() + ESPERA_MAXIMA_S
    while time.monotonic() < limite:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT count(*) FROM pg_stat_activity "
                "WHERE wait_event_type = 'Lock' AND datname = current_database()"
            )
            if cursor.fetchone()[0]:
                return
        time.sleep(0.02)
    pytest.fail("nenhuma conexão ficou esperando a trava do espaço")


def _cadastrar_espaco(nome: str = "Ginásio A") -> int:
    return RepositorioEspacosDjango().salvar(novo_espaco(nome=nome)).id


def _data_futura():
    return timezone.localdate() + timedelta(days=3)


def _reservar_das_21_as_22(espaco_id: int, pedido: CriarReserva | None = None):
    return (pedido or criar_reserva()).executar(
        espaco_id=espaco_id,
        solicitante=ANA,
        data=_data_futura(),
        hora_inicio=hora(21, 0),
        hora_fim=hora(22, 0),
        finalidade="Treino",
    )


def _editar_fechamento_para_20h(espaco_id: int, reservas):
    return EditarEspaco(RepositorioEspacosDjango(), reservas).executar(
        espaco_id, fechamento=hora(20, 0)
    )


def _reservas_fora_da_janela() -> list[str]:
    problemas = []
    espacos = {e.pk: e for e in EspacoEsportivoModel.objects.all()}
    for reserva in ReservaModel.objects.filter(
        situacao__in=["SOLICITADA", "CONFIRMADA"]
    ):
        espaco = espacos[reserva.espaco_id]
        inicio = reserva.inicio.astimezone(FUSO)
        fim = reserva.fim.astimezone(FUSO)
        meia_noite = inicio.replace(hour=0, minute=0, second=0, microsecond=0)
        inicio_min = (inicio - meia_noite) // timedelta(minutes=1)
        fim_min = (fim - meia_noite) // timedelta(minutes=1)
        if (
            inicio_min < espaco.abertura_em_minutos
            or fim_min > espaco.fechamento_em_minutos
        ):
            problemas.append(
                f"reserva {reserva.pk} ({inicio_min}–{fim_min} min) fora do horário "
                f"do espaço ({espaco.abertura_em_minutos}–"
                f"{espaco.fechamento_em_minutos} min)"
            )
    return problemas


@pytest.mark.django_db(transaction=True)
def test_edicao_do_horario_em_andamento_faz_a_criacao_esperar_e_ser_recusada():
    # Arrange
    espaco_id = _cadastrar_espaco()
    sinais = _Sinais()
    resultados: dict = {}

    # Act
    edicao = _em_thread(
        resultados,
        "edicao",
        lambda: _editar_fechamento_para_20h(espaco_id, _ContagemPausada(sinais)),
    )
    assert sinais.pausada.wait(ESPERA_MAXIMA_S), "a edição não chegou à pausa"
    criacao = _em_thread(
        resultados, "criacao", lambda: _reservar_das_21_as_22(espaco_id)
    )
    _esperar_alguem_esperando_uma_trava()
    terminou_antes = "criacao" in resultados
    sinais.liberar.set()
    edicao.join(timeout=ESPERA_MAXIMA_S)
    criacao.join(timeout=ESPERA_MAXIMA_S)

    # Assert
    assert not terminou_antes, "a criação não esperou a edição"
    assert set(resultados) == {"edicao", "criacao"}, "uma das threads não terminou"
    assert resultados["edicao"].horario.fechamento_em_minutos == 20 * 60
    assert isinstance(resultados["criacao"], ForaDoHorarioDeFuncionamento)
    assert _reservas_fora_da_janela() == []
    assert ReservaModel.objects.count() == 0


@pytest.mark.django_db(transaction=True)
def test_criacao_em_andamento_faz_a_edicao_do_horario_esperar_e_ser_recusada():
    # Arrange
    espaco_id = _cadastrar_espaco()
    sinais = _Sinais()
    resultados: dict = {}
    pedido = CriarReserva(
        RepositorioReservasDjango(), _LeituraDoEspacoPausada(sinais), timezone.now
    )

    # Act
    criacao = _em_thread(
        resultados, "criacao", lambda: _reservar_das_21_as_22(espaco_id, pedido)
    )
    assert sinais.pausada.wait(ESPERA_MAXIMA_S), "a criação não chegou à pausa"
    edicao = _em_thread(
        resultados,
        "edicao",
        lambda: _editar_fechamento_para_20h(espaco_id, ReservasDoEspacoViaCasoDeUso()),
    )
    _esperar_alguem_esperando_uma_trava()
    terminou_antes = "edicao" in resultados
    sinais.liberar.set()
    criacao.join(timeout=ESPERA_MAXIMA_S)
    edicao.join(timeout=ESPERA_MAXIMA_S)

    # Assert
    assert not terminou_antes, "a edição não esperou a criação"
    assert set(resultados) == {"edicao", "criacao"}, "uma das threads não terminou"
    assert resultados["criacao"].espaco_id == espaco_id
    assert isinstance(resultados["edicao"], HorarioIncompativelComReservas)
    assert resultados["edicao"].codigo == "HORARIO_INCOMPATIVEL_COM_RESERVAS"
    horario = RepositorioEspacosDjango().obter_por_id(espaco_id).horario
    assert horario.fechamento_em_minutos == 24 * 60
    assert _reservas_fora_da_janela() == []


@pytest.mark.django_db(transaction=True)
def test_criacoes_em_espacos_diferentes_nao_se_bloqueiam():
    # Arrange
    primeiro = _cadastrar_espaco("Ginásio A")
    segundo = _cadastrar_espaco("Ginásio B")
    sinais = _Sinais()
    resultados: dict = {}
    pedido = CriarReserva(
        RepositorioReservasDjango(), _LeituraDoEspacoPausada(sinais), timezone.now
    )

    # Act
    criacao_pausada = _em_thread(
        resultados, "primeiro", lambda: _reservar_das_21_as_22(primeiro, pedido)
    )
    assert sinais.pausada.wait(ESPERA_MAXIMA_S), "a criação não chegou à pausa"
    outra = _em_thread(resultados, "segundo", lambda: _reservar_das_21_as_22(segundo))
    outra.join(timeout=ESPERA_MAXIMA_S)
    segundo_terminou_com_a_primeira_pausada = "segundo" in resultados
    sinais.liberar.set()
    criacao_pausada.join(timeout=ESPERA_MAXIMA_S)

    # Assert
    assert segundo_terminou_com_a_primeira_pausada, (
        "o segundo espaço esperou o primeiro"
    )
    assert resultados["segundo"].espaco_id == segundo
    assert resultados["primeiro"].espaco_id == primeiro
