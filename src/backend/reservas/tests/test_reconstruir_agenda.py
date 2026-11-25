from datetime import date, datetime, time, timedelta

import pytest

from reservas.application.ocupacao_do_dia import HorarioOcupado
from reservas.application.portas import AgendaIndisponivel
from reservas.application.reconstruir_agenda import (
    TENTATIVAS_POR_DIA,
    ReconstruirAgenda,
    ResultadoDaReconstrucao,
)
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import (
    AGORA,
    DIA,
    GESTOR,
    MOTIVO,
    UTC,
    AgendaDoDiaEmMemoria,
    RepositorioReservasEmMemoria,
    intervalo,
    reserva_solicitada,
)

S = SituacaoReserva
OUTRO_DIA = DIA + timedelta(days=1)
ONTEM = AGORA.date() - timedelta(days=1)


def _guardar(repositorio, *, espaco_id=3, data=DIA, inicio=10, situacao=S.SOLICITADA):
    reserva = repositorio.salvar(
        reserva_solicitada(
            espaco_id=espaco_id,
            data=data,
            hora_inicio=time(inicio, 0),
            hora_fim=time(inicio + 1, 0),
        )
    )
    if situacao is S.CONFIRMADA:
        reserva.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=AGORA)
    elif situacao is S.CANCELADA:
        reserva.alterar_situacao(S.CANCELADA, motivo=MOTIVO, ator=GESTOR, agora=AGORA)
    return repositorio.salvar(reserva)


def _ocupado(inicio, situacao=S.SOLICITADA, data=DIA):
    return HorarioOcupado(
        intervalo(f"{inicio:02d}:00", f"{inicio + 1:02d}:00", data), situacao
    )


def _reconstruir(repositorio, agenda, agora=AGORA):
    return ReconstruirAgenda(repositorio, agenda, lambda: agora).executar()


def test_reconstroi_de_uma_agenda_vazia_varios_espacos_e_datas():
    # Arrange
    repositorio, agenda = RepositorioReservasEmMemoria(), AgendaDoDiaEmMemoria()
    _guardar(repositorio, espaco_id=3, data=DIA, inicio=10)
    _guardar(repositorio, espaco_id=3, data=DIA, inicio=14, situacao=S.CONFIRMADA)
    _guardar(repositorio, espaco_id=3, data=OUTRO_DIA, inicio=9)
    _guardar(repositorio, espaco_id=4, data=DIA, inicio=8)

    # Act
    resultado = _reconstruir(repositorio, agenda)

    # Assert
    assert resultado == ResultadoDaReconstrucao(
        dias_refeitos=3, reservas_gravadas=4, dias_esvaziados=0, dias_descartados=0
    )
    assert agenda.listar(3, DIA) == (_ocupado(10), _ocupado(14, S.CONFIRMADA))
    assert agenda.listar(3, OUTRO_DIA) == (_ocupado(9, data=OUTRO_DIA),)
    assert agenda.listar(4, DIA) == (_ocupado(8),)


def test_a_segunda_execucao_deixa_a_agenda_e_o_resultado_iguais():
    # Arrange
    repositorio, agenda = RepositorioReservasEmMemoria(), AgendaDoDiaEmMemoria()
    _guardar(repositorio, inicio=10)
    _guardar(repositorio, espaco_id=4, data=OUTRO_DIA, inicio=9)
    agenda.substituir(3, DIA, {99: _ocupado(20)}, versao=0)
    primeira = _reconstruir(repositorio, agenda)
    estado = {c: agenda.listar(*c) for c in agenda.dias_projetados(ONTEM)}

    # Act
    segunda = _reconstruir(repositorio, agenda)

    # Assert
    assert segunda == primeira
    assert {c: agenda.listar(*c) for c in agenda.dias_projetados(ONTEM)} == estado


def test_corrige_membro_de_reserva_cancelada_e_membro_que_faltava():
    # Arrange
    repositorio, agenda = RepositorioReservasEmMemoria(), AgendaDoDiaEmMemoria()
    cancelada = _guardar(repositorio, inicio=10, situacao=S.CANCELADA)
    _guardar(repositorio, inicio=14)
    agenda.substituir(3, DIA, {cancelada.id: _ocupado(10)}, versao=0)

    # Act
    _reconstruir(repositorio, agenda)

    # Assert
    assert agenda.listar(3, DIA) == (_ocupado(14),)


def test_dia_projetado_sem_reserva_ativa_vira_vazio_e_conta_como_esvaziado():
    # Arrange
    repositorio, agenda = RepositorioReservasEmMemoria(), AgendaDoDiaEmMemoria()
    agenda.substituir(3, DIA, {5: _ocupado(10)}, versao=0)

    # Act
    resultado = _reconstruir(repositorio, agenda)

    # Assert
    assert agenda.listar(3, DIA) == ()
    assert resultado == ResultadoDaReconstrucao(dias_refeitos=1, dias_esvaziados=1)


def test_dia_projetado_que_ja_estava_vazio_nao_conta_como_esvaziado():
    # Arrange
    repositorio, agenda = RepositorioReservasEmMemoria(), AgendaDoDiaEmMemoria()
    agenda.substituir(3, DIA, {}, versao=0)

    # Act
    resultado = _reconstruir(repositorio, agenda)

    # Assert
    assert agenda.listar(3, DIA) == ()
    assert resultado == ResultadoDaReconstrucao(dias_refeitos=1)


def test_dia_anterior_a_hoje_nao_e_tocado():
    # Arrange
    repositorio, agenda = RepositorioReservasEmMemoria(), AgendaDoDiaEmMemoria()
    agenda.substituir(3, ONTEM, {5: _ocupado(10, data=ONTEM)}, versao=0)

    # Act
    resultado = _reconstruir(repositorio, agenda)

    # Assert
    assert agenda.listar(3, ONTEM) == (_ocupado(10, data=ONTEM),)
    assert resultado == ResultadoDaReconstrucao()


def test_hoje_e_a_data_de_brasilia_mesmo_quando_o_utc_ja_e_o_dia_seguinte():
    # Arrange
    repositorio, agenda = RepositorioReservasEmMemoria(), AgendaDoDiaEmMemoria()
    _guardar(repositorio, data=DIA, inicio=10)
    utc_ja_no_dia_seguinte = datetime(2026, 10, 26, 1, 0, tzinfo=UTC)

    # Act
    resultado = _reconstruir(repositorio, agenda, utc_ja_no_dia_seguinte)

    # Assert
    assert resultado.dias_refeitos == 1
    assert agenda.listar(3, DIA) == (_ocupado(10),)


def test_so_reservas_solicitadas_e_confirmadas_entram():
    # Arrange
    repositorio, agenda = RepositorioReservasEmMemoria(), AgendaDoDiaEmMemoria()
    _guardar(repositorio, inicio=8, situacao=S.SOLICITADA)
    _guardar(repositorio, inicio=10, situacao=S.CONFIRMADA)
    _guardar(repositorio, inicio=12, situacao=S.CANCELADA)

    # Act
    resultado = _reconstruir(repositorio, agenda)

    # Assert
    assert resultado.reservas_gravadas == 2
    assert agenda.listar(3, DIA) == (_ocupado(8), _ocupado(10, S.CONFIRMADA))


class AgendaQueMudaNoMeio(AgendaDoDiaEmMemoria):
    def __init__(self, *, mudancas: int) -> None:
        super().__init__()
        self._mudancas = mudancas

    def substituir(self, espaco_id, data, ocupados, *, versao):
        if self._mudancas > 0:
            self._mudancas -= 1
            self.remover(espaco_id, 999, data)
        return super().substituir(espaco_id, data, ocupados, versao=versao)


def test_versao_que_avanca_no_meio_faz_nova_tentativa_e_grava():
    # Arrange
    repositorio = RepositorioReservasEmMemoria()
    agenda = AgendaQueMudaNoMeio(mudancas=1)
    _guardar(repositorio, inicio=10)

    # Act
    resultado = _reconstruir(repositorio, agenda)

    # Assert
    assert resultado == ResultadoDaReconstrucao(dias_refeitos=1, reservas_gravadas=1)
    assert agenda.listar(3, DIA) == (_ocupado(10),)


def test_versao_que_avanca_sempre_descarta_o_dia_sem_lancar_e_segue_para_o_proximo():
    # Arrange: só o primeiro dia sofre mudanças, tantas quantas as tentativas
    repositorio = RepositorioReservasEmMemoria()
    agenda = AgendaQueMudaNoMeio(mudancas=TENTATIVAS_POR_DIA)
    _guardar(repositorio, data=DIA, inicio=10)
    _guardar(repositorio, data=OUTRO_DIA, inicio=10)

    # Act
    resultado = _reconstruir(repositorio, agenda)

    # Assert
    assert resultado == ResultadoDaReconstrucao(
        dias_refeitos=1, reservas_gravadas=1, dias_descartados=1
    )
    assert agenda.listar(3, DIA) is None
    assert agenda.listar(3, OUTRO_DIA) == (_ocupado(10, data=OUTRO_DIA),)


class AgendaQueFalhaEm(AgendaDoDiaEmMemoria):
    def __init__(self, operacao: str) -> None:
        super().__init__()
        self._operacao = operacao

    def dias_projetados(self, a_partir_de: date):
        self._falhar_se("dias_projetados")
        return super().dias_projetados(a_partir_de)

    def versao(self, espaco_id, data):
        self._falhar_se("versao")
        return super().versao(espaco_id, data)

    def substituir(self, espaco_id, data, ocupados, *, versao):
        self._falhar_se("substituir")
        return super().substituir(espaco_id, data, ocupados, versao=versao)

    def _falhar_se(self, operacao: str) -> None:
        if operacao == self._operacao:
            raise AgendaIndisponivel


@pytest.mark.parametrize("operacao", ["dias_projetados", "versao", "substituir"])
def test_agenda_indisponivel_sobe_sem_ser_engolida(operacao):
    # Arrange
    repositorio = RepositorioReservasEmMemoria()
    _guardar(repositorio, inicio=10)

    # Act / Assert
    with pytest.raises(AgendaIndisponivel):
        _reconstruir(repositorio, AgendaQueFalhaEm(operacao))
