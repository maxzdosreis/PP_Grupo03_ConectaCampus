import contextlib
from datetime import date, datetime, time, timedelta

from hypothesis import settings
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, invariant, rule

from reservas.application.casos_de_uso import AlterarSituacaoReserva, CriarReserva
from reservas.application.ocupacao_do_dia import HorarioOcupado, ocupados_por_reserva
from reservas.application.reconstruir_agenda import ReconstruirAgenda
from reservas.application.reconstruir_indice import ReconstruirIndice
from reservas.domain.excecoes import ConflitoDeHorario, TransicaoDeSituacaoInvalida
from reservas.domain.situacao import SITUACOES_QUE_EXIGEM_MOTIVO, SituacaoReserva
from reservas.infrastructure.repositorio_com_agenda import RepositorioReservasComAgenda
from reservas.tests.fakes import (
    AGORA,
    ANA,
    GESTOR,
    MOTIVO,
    AgendaDoDiaEmMemoria,
    ConsultaDeEspacosEmMemoria,
    IndiceDeReservasEmMemoria,
    RepositorioReservasEmMemoria,
    espaco_reservavel,
)

S = SituacaoReserva
ESPACOS = (1, 2)
DIAS = (date(2026, 10, 25), date(2026, 10, 26))
MINUTOS_NO_DIA = 24 * 60
PASSOS = 30
DESTINOS = [S.CONFIRMADA, S.RECUSADA, S.CANCELADA]


def _hora(minutos: int) -> time:
    return time(minutos // 60 % 24, minutos % 60)


def _ordenados(ocupados) -> list[HorarioOcupado]:
    return sorted(
        ocupados,
        key=lambda o: (o.intervalo.hora_inicio, o.intervalo.hora_fim, o.situacao.value),
    )


class MaquinaDasProjecoes(RuleBasedStateMachine):
    def __init__(self) -> None:
        super().__init__()
        self.agora: datetime = AGORA
        self.acoes_adiadas: list = []
        self.repositorio = RepositorioReservasEmMemoria()
        self.agenda = AgendaDoDiaEmMemoria()
        self.indice = IndiceDeReservasEmMemoria()
        decorator = RepositorioReservasComAgenda(
            self.repositorio,
            self.agenda,
            self.indice,
            apos_o_commit=self.acoes_adiadas.append,
        )
        consulta = ConsultaDeEspacosEmMemoria(
            [espaco_reservavel(i, f"Quadra {i}") for i in ESPACOS]
        )
        self.criar = CriarReserva(decorator, consulta, lambda: self.agora)
        self.alterar = AlterarSituacaoReserva(decorator, lambda: self.agora)
        for espaco_id in ESPACOS:
            for dia in DIAS:
                versao = self.agenda.versao(espaco_id, dia)
                assert self.agenda.substituir(espaco_id, dia, {}, versao=versao)
        self._reconstruir_o_indice()

    @rule(
        espaco_id=st.sampled_from(ESPACOS),
        dia=st.sampled_from(DIAS),
        inicio=st.integers(7 * 60 // PASSOS, MINUTOS_NO_DIA // PASSOS - 1),
        duracao=st.sampled_from([30, 60, 90, 120, 180]),
    )
    def solicitar(self, espaco_id, dia, inicio, duracao):
        comeco = inicio * PASSOS
        fim = comeco + duracao
        if fim > MINUTOS_NO_DIA:
            return
        self._avancar_o_relogio()
        with contextlib.suppress(ConflitoDeHorario):
            self.criar.executar(
                espaco_id=espaco_id,
                solicitante=ANA,
                data=dia,
                hora_inicio=_hora(comeco),
                hora_fim=_hora(fim),
                finalidade="Treino",
            )

    @rule(posicao=st.integers(0, 50), destino=st.sampled_from(DESTINOS))
    def mudar_a_situacao(self, posicao, destino):
        reserva_id = self._reserva_na_posicao(posicao)
        if reserva_id is None:
            return
        self._avancar_o_relogio()
        motivo = MOTIVO if destino in SITUACOES_QUE_EXIGEM_MOTIVO else None
        with contextlib.suppress(TransicaoDeSituacaoInvalida):
            self.alterar.executar(
                reserva_id=reserva_id, nova_situacao=destino, motivo=motivo, ator=GESTOR
            )

    @rule(posicao=st.integers(0, 50))
    def executar_uma_acao_adiada(self, posicao):
        if self.acoes_adiadas:
            self.acoes_adiadas.pop(posicao % len(self.acoes_adiadas))()

    @rule()
    def executar_as_acoes_adiadas_do_fim_para_o_comeco(self):
        while self.acoes_adiadas:
            self.acoes_adiadas.pop()()

    @rule()
    def reconstruir_nao_muda_o_que_ja_convergiu(self):
        while self.acoes_adiadas:
            self.acoes_adiadas.pop(0)()
        antes = self._retrato()
        self._reconstruir_tudo()
        depois_da_primeira = self._retrato()
        self._reconstruir_tudo()
        assert antes == depois_da_primeira == self._retrato()

    @invariant()
    def sem_acoes_adiadas_as_projecoes_dizem_o_mesmo_que_o_repositorio(self):
        if self.acoes_adiadas:
            return
        for espaco_id in ESPACOS:
            for dia in DIAS:
                assert self._agenda_do_dia(espaco_id, dia) == self._ocupados_do_dia(
                    espaco_id, dia
                ), (espaco_id, dia)
        fila, contagem = self._fila_e_contagem_do_repositorio()
        assert self.indice.pendentes(10_000) == fila
        assert self.indice.contagem_por_situacao() == contagem

    def _avancar_o_relogio(self):
        self.agora += timedelta(minutes=1)

    def _reserva_na_posicao(self, posicao):
        ids = [r.reserva_id for r in self.repositorio.listar_para_indice(0, 10_000)]
        return ids[posicao % len(ids)] if ids else None

    def _reconstruir_o_indice(self):
        resultado = ReconstruirIndice(self.repositorio, self.indice).executar()
        assert not resultado.descartado

    def _reconstruir_tudo(self):
        ReconstruirAgenda(self.repositorio, self.agenda, lambda: self.agora).executar()
        self._reconstruir_o_indice()

    def _agenda_do_dia(self, espaco_id, dia):
        return _ordenados(self.agenda.listar(espaco_id, dia) or ())

    def _ocupados_do_dia(self, espaco_id, dia):
        reservas = self.repositorio.listar_que_ocupam_horario(espaco_id, dia)
        return _ordenados(ocupados_por_reserva(reservas).values())

    def _fila_e_contagem_do_repositorio(self):
        registros = self.repositorio.listar_para_indice(0, 10_000)
        solicitadas = sorted(
            (r for r in registros if r.situacao is S.SOLICITADA),
            key=lambda r: (r.criada_em.timestamp(), r.reserva_id),
        )
        situacoes = [r.situacao for r in registros]
        contagem = {s: situacoes.count(s) for s in SituacaoReserva}
        return tuple(r.reserva_id for r in solicitadas), contagem

    def _retrato(self):
        agendas = {(e, d): self._agenda_do_dia(e, d) for e in ESPACOS for d in DIAS}
        return (
            agendas,
            self.indice.pendentes(10_000),
            self.indice.contagem_por_situacao(),
        )


TestMaquinaDasProjecoes = MaquinaDasProjecoes.TestCase
TestMaquinaDasProjecoes.settings = settings(stateful_step_count=25, deadline=None)
