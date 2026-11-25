from datetime import time, timedelta

import pytest
from django.utils import timezone

from reservas.application.casos_de_uso import AlterarSituacaoReserva, CriarReserva
from reservas.application.reconstruir_agenda import ReconstruirAgenda
from reservas.application.reconstruir_indice import ReconstruirIndice
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.agenda_redis import AgendaDoDiaRedis
from reservas.infrastructure.consulta_de_espacos import ConsultaDeEspacosViaFachada
from reservas.infrastructure.indice_redis import IndiceDeReservasRedis
from reservas.infrastructure.repositorio_com_agenda import RepositorioReservasComAgenda
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango
from reservas.tests.fakes import ANA, FUNCIONAMENTO_PADRAO, GESTOR
from reservas.tests.redis_de_teste import (
    afirmar_indice_igual_ao_postgres,
    ocupados_do_postgres,
    ocupados_do_redis,
    redis_limpo_depois,
)

pytestmark = [
    pytest.mark.django_db,
    pytest.mark.usefixtures("redis_limpo_depois"),
]

S = SituacaoReserva
CRIAR = "criar"
CANCELAR = "cancelar"


def _amanha():
    return timezone.localdate() + timedelta(days=1)


def _guardar(espaco_id, hora):
    reserva = Reserva.solicitar(
        espaco_id=espaco_id,
        solicitante=ANA,
        data=_amanha(),
        hora_inicio=time(hora, 0),
        hora_fim=time(hora + 1, 0),
        finalidade="Treino do time",
        agora=timezone.now(),
        funcionamento=FUNCIONAMENTO_PADRAO,
    )
    return RepositorioReservasDjango().salvar(reserva)


def _com_agenda():
    return RepositorioReservasComAgenda(
        RepositorioReservasDjango(),
        AgendaDoDiaRedis(),
        IndiceDeReservasRedis(),
        apos_o_commit=lambda acao: acao(),
    )


def _criar_pelo_decorator(espaco_id):
    CriarReserva(_com_agenda(), ConsultaDeEspacosViaFachada(), timezone.now).executar(
        espaco_id=espaco_id,
        solicitante=ANA,
        data=_amanha(),
        hora_inicio=time(14, 0),
        hora_fim=time(15, 0),
        finalidade="Treino",
    )


def _mudar_pelo_decorator(reserva_id, nova, motivo=None):
    AlterarSituacaoReserva(_com_agenda(), timezone.now).executar(
        reserva_id=reserva_id, nova_situacao=nova, motivo=motivo, ator=GESTOR
    )


def _cancelar_pelo_decorator(reserva_id):
    _mudar_pelo_decorator(reserva_id, S.CANCELADA, "Quadra interditada")


class _RepositorioQueMexeNoMeio(RepositorioReservasDjango):
    """Faz `acao` uma única vez, logo depois da leitura de número `na_leitura`."""

    def __init__(self, metodo, na_leitura, acao):
        self._metodo = metodo
        self._na_leitura = na_leitura
        self._acao = acao
        self._leituras = 0
        self.acoes_feitas = 0

    def listar_que_ocupam_horario(self, espaco_id, data):
        reservas = super().listar_que_ocupam_horario(espaco_id, data)
        self._depois_de_ler("listar_que_ocupam_horario")
        return reservas

    def listar_para_indice(self, depois_de_id, limite):
        registros = super().listar_para_indice(depois_de_id, limite)
        if registros:
            self._depois_de_ler("listar_para_indice")
        return registros

    def _depois_de_ler(self, metodo):
        if metodo != self._metodo:
            return
        self._leituras += 1
        if self._leituras == self._na_leitura:
            self.acoes_feitas += 1
            self._acao()


@pytest.mark.parametrize("na_leitura", [1, 2], ids=["1a_leitura", "retrato_2a_leitura"])
@pytest.mark.parametrize("escrita", [CRIAR, CANCELAR])
def test_agenda_reconstruida_com_escrita_no_meio_termina_igual_ao_postgresql(
    espaco_id, escrita, na_leitura
):
    # Arrange
    existente = _guardar(espaco_id, 10)
    ReconstruirAgenda(
        RepositorioReservasDjango(), AgendaDoDiaRedis(), timezone.now
    ).executar()
    assert ocupados_do_redis(espaco_id, _amanha()) == ocupados_do_postgres(
        espaco_id, _amanha()
    )
    acao = (
        (lambda: _criar_pelo_decorator(espaco_id))
        if escrita == CRIAR
        else (lambda: _cancelar_pelo_decorator(existente.id))
    )
    repositorio = _RepositorioQueMexeNoMeio(
        "listar_que_ocupam_horario", na_leitura, acao
    )

    # Act
    resultado = ReconstruirAgenda(
        repositorio, AgendaDoDiaRedis(), timezone.now
    ).executar()

    # Assert
    assert repositorio.acoes_feitas == 1
    assert resultado.dias_descartados == 0
    assert resultado.dias_refeitos == 1
    esperado = ocupados_do_postgres(espaco_id, _amanha())
    assert len(esperado) == (2 if escrita == CRIAR else 0)
    assert ocupados_do_redis(espaco_id, _amanha()) == esperado


@pytest.mark.parametrize("escrita", [CRIAR, "confirmar", CANCELAR])
def test_indice_reconstruido_com_mudanca_no_meio_nao_perde_a_mudanca(
    espaco_id, escrita
):
    # Arrange
    primeira = _guardar(espaco_id, 9)
    _guardar(espaco_id, 11)
    _guardar(espaco_id, 16)
    acoes = {
        CRIAR: lambda: _criar_pelo_decorator(espaco_id),
        "confirmar": lambda: _mudar_pelo_decorator(primeira.id, S.CONFIRMADA),
        CANCELAR: lambda: _cancelar_pelo_decorator(primeira.id),
    }
    ReconstruirIndice(RepositorioReservasDjango(), IndiceDeReservasRedis()).executar()
    afirmar_indice_igual_ao_postgres()
    repositorio = _RepositorioQueMexeNoMeio("listar_para_indice", 1, acoes[escrita])

    # Act
    resultado = ReconstruirIndice(repositorio, IndiceDeReservasRedis()).executar()

    # Assert
    assert repositorio.acoes_feitas == 1
    assert not resultado.descartado
    fila = afirmar_indice_igual_ao_postgres()
    assert (primeira.id in fila) == (escrita == CRIAR)
    assert len(fila) == {CRIAR: 4, "confirmar": 2, CANCELAR: 2}[escrita]
