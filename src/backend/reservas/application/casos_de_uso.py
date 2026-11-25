import logging
from collections.abc import Callable
from contextlib import suppress
from dataclasses import replace
from datetime import date, datetime, time

from compartilhado.domain.erros import ErroDeDominio
from reservas.application.ocupacao_do_dia import HorarioOcupado, OcupacaoDoDia
from reservas.application.portas import (
    AgendaDoDia,
    AgendaIndisponivel,
    ConsultaDeEspacos,
)
from reservas.application.repositorio import (
    FiltrosDeReservas,
    Paginacao,
    PaginaDeReservas,
    RepositorioReservas,
)
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.conflito_de_horario import garantir_horario_livre
from reservas.domain.excecoes import ReservaNaoEncontrada
from reservas.domain.funcionamento import FuncionamentoDoEspaco
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.registro_de_situacao import RegistroDeSituacao
from reservas.domain.regras_de_agenda import (
    garantir_inicio_no_futuro,
    horarios_livres,
    motivo_de_indisponibilidade,
)
from reservas.domain.reserva import Reserva, validar_espaco_id
from reservas.domain.situacao import SituacaoReserva
from reservas.domain.solicitante import Solicitante

logger = logging.getLogger(__name__)


class CriarReserva:
    def __init__(
        self,
        repositorio: RepositorioReservas,
        consulta_de_espacos: ConsultaDeEspacos,
        relogio: Callable[[], datetime],
    ) -> None:
        self._repositorio = repositorio
        self._consulta_de_espacos = consulta_de_espacos
        self._relogio = relogio

    def executar(
        self,
        *,
        espaco_id: int,
        solicitante: Solicitante,
        data: date,
        hora_inicio: time,
        hora_fim: time,
        finalidade: str,
    ) -> Reserva:
        agora = self._relogio()
        pedido = IntervaloDeHorario(
            data=data, hora_inicio=hora_inicio, hora_fim=hora_fim
        )
        garantir_inicio_no_futuro(pedido, agora)
        validar_espaco_id(espaco_id)
        with self._repositorio.em_transacao():
            espaco = self._consulta_de_espacos.obter_espaco_reservavel_travado(
                espaco_id
            )
            reserva = Reserva.solicitar(
                espaco_id=espaco_id,
                solicitante=solicitante,
                data=data,
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
                finalidade=finalidade,
                agora=agora,
                funcionamento=espaco.funcionamento,
            )
            existentes = self._repositorio.listar_que_ocupam_horario(
                reserva.espaco_id, reserva.intervalo.data
            )
            garantir_horario_livre(reserva, existentes)
            return self._repositorio.salvar(reserva)


class ConsultarReservas:
    def __init__(self, repositorio: RepositorioReservas) -> None:
        self._repositorio = repositorio

    def executar(
        self, filtros: FiltrosDeReservas, paginacao: Paginacao, *, ator: Ator
    ) -> PaginaDeReservas:
        return self._repositorio.listar(_restringir_ao_ator(filtros, ator), paginacao)


class ObterReserva:
    def __init__(self, repositorio: RepositorioReservas) -> None:
        self._repositorio = repositorio

    def executar(self, reserva_id: int, *, ator: Ator) -> Reserva:
        return _obter_ou_falhar(self._repositorio, reserva_id, ator)


class AlterarSituacaoReserva:
    def __init__(
        self, repositorio: RepositorioReservas, relogio: Callable[[], datetime]
    ) -> None:
        self._repositorio = repositorio
        self._relogio = relogio

    def executar(
        self,
        *,
        reserva_id: int,
        nova_situacao: SituacaoReserva | str,
        motivo: str | None = None,
        ator: Ator,
    ) -> Reserva:
        reserva = _obter_ou_falhar(self._repositorio, reserva_id, ator)
        agora = self._relogio()
        try:
            reserva.alterar_situacao(
                nova_situacao, motivo=motivo, ator=ator, agora=agora
            )
            return self._repositorio.salvar(reserva)
        except ErroDeDominio as erro:
            if _foi_pedida_uma_situacao(nova_situacao):
                self._registrar_tentativa(
                    reserva_id, nova_situacao, motivo, ator, agora, erro
                )
            raise

    def _registrar_tentativa(
        self,
        reserva_id: int,
        nova_situacao: SituacaoReserva | str,
        motivo: str | None,
        ator: Ator,
        agora: datetime,
        erro: ErroDeDominio,
    ) -> None:
        try:
            atual = _obter_ou_falhar(self._repositorio, reserva_id, ator)
            registro = atual.registrar_tentativa_recusada(
                nova_situacao,
                motivo=motivo,
                ator=ator,
                agora=agora,
                codigo_do_erro=erro.codigo,
            )
            self._repositorio.gravar_tentativa_recusada(reserva_id, registro)
        except Exception:
            logger.exception(
                "Não foi possível registrar a tentativa recusada na reserva %s.",
                reserva_id,
            )


def _foi_pedida_uma_situacao(nova_situacao: SituacaoReserva | str | None) -> bool:
    return bool(str(nova_situacao or "").strip())


class ConsultarHistoricoDaReserva:
    def __init__(self, repositorio: RepositorioReservas) -> None:
        self._repositorio = repositorio

    def executar(self, reserva_id: int, *, ator: Ator) -> list[RegistroDeSituacao]:
        _obter_ou_falhar(self._repositorio, reserva_id, ator)
        return self._repositorio.listar_historico(reserva_id)


class ConsultarOcupacaoDoDia:
    def __init__(
        self,
        repositorio: RepositorioReservas,
        consulta_de_espacos: ConsultaDeEspacos,
        agenda: AgendaDoDia,
        relogio: Callable[[], datetime],
    ) -> None:
        self._repositorio = repositorio
        self._consulta_de_espacos = consulta_de_espacos
        self._agenda = agenda
        self._relogio = relogio

    def executar(self, *, espaco_id: int, data: date) -> OcupacaoDoDia:
        funcionamento = self._consulta_de_espacos.obter_espaco_reservavel(
            espaco_id
        ).funcionamento
        ocupados = self._ocupados_do_dia(espaco_id, data)
        agora = self._relogio()
        motivo = motivo_de_indisponibilidade(data, agora, funcionamento)
        livres = horarios_livres(
            [ocupado.intervalo for ocupado in ocupados],
            data=data,
            agora=agora,
            funcionamento=funcionamento,
        )
        return OcupacaoDoDia(
            data=data,
            horario_de_abertura=funcionamento.abertura(),
            horario_de_fechamento=funcionamento.fechamento(),
            ocupados=ocupados,
            livres=() if motivo else tuple(livres),
            reservavel=motivo is None,
            motivo_indisponivel=motivo,
        )

    def _ocupados_do_dia(
        self, espaco_id: int, data: date
    ) -> tuple[HorarioOcupado, ...]:
        try:
            agendados = self._agenda.listar(espaco_id, data)
        except AgendaIndisponivel:
            return tuple(self._do_postgres(espaco_id, data).values())
        if agendados is not None:
            return agendados
        return self._repovoar(espaco_id, data)

    def _repovoar(self, espaco_id: int, data: date) -> tuple[HorarioOcupado, ...]:
        try:
            versao = self._agenda.versao(espaco_id, data)
        except AgendaIndisponivel:
            return tuple(self._do_postgres(espaco_id, data).values())
        ocupados = self._do_postgres(espaco_id, data)
        with suppress(AgendaIndisponivel):
            self._agenda.substituir(espaco_id, data, ocupados, versao=versao)
        return tuple(ocupados.values())

    def _do_postgres(self, espaco_id: int, data: date) -> dict[int, HorarioOcupado]:
        reservas = self._repositorio.listar_que_ocupam_horario(espaco_id, data)
        return {
            reserva.id: _ao_minuto(reserva.intervalo, reserva.situacao)
            for reserva in reservas
        }


def _ao_minuto(
    intervalo: IntervaloDeHorario, situacao: SituacaoReserva
) -> HorarioOcupado:
    return HorarioOcupado(
        intervalo=IntervaloDeHorario(
            data=intervalo.data,
            hora_inicio=intervalo.hora_inicio.replace(second=0, microsecond=0),
            hora_fim=intervalo.hora_fim.replace(second=0, microsecond=0),
        ),
        situacao=situacao,
    )


class ContarReservasAtivasForaDaJanela:
    def __init__(
        self, repositorio: RepositorioReservas, relogio: Callable[[], datetime]
    ) -> None:
        self._repositorio = repositorio
        self._relogio = relogio

    def executar(
        self, espaco_id: int, abertura_em_minutos: int, fechamento_em_minutos: int
    ) -> int:
        janela = FuncionamentoDoEspaco(abertura_em_minutos, fechamento_em_minutos)
        ativas = self._repositorio.listar_ativas_a_partir_de(espaco_id, self._relogio())
        return sum(1 for reserva in ativas if not _cabe_na_janela(reserva, janela))


def _cabe_na_janela(reserva: Reserva, janela: FuncionamentoDoEspaco) -> bool:
    intervalo = reserva.intervalo
    return janela.abre_em(
        intervalo.data
    ) <= intervalo.inicio() and intervalo.fim() <= janela.fecha_em(intervalo.data)


def _restringir_ao_ator(filtros: FiltrosDeReservas, ator: Ator) -> FiltrosDeReservas:
    if ator.papel is PapelDoAtor.GESTOR:
        return filtros
    return replace(filtros, solicitante_usuario_id=ator.usuario_id)


def _obter_ou_falhar(
    repositorio: RepositorioReservas, reserva_id: int, ator: Ator
) -> Reserva:
    reserva = repositorio.obter_por_id(reserva_id)
    if reserva is None or not reserva.visivel_para(ator):
        raise ReservaNaoEncontrada(reserva_id)
    return reserva
