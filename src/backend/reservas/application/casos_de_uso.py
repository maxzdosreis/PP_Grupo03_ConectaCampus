from collections.abc import Callable
from dataclasses import replace
from datetime import date, datetime, time

from reservas.application.portas import ConsultaDeEspacos
from reservas.application.repositorio import FiltrosDeReservas, RepositorioReservas
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.conflito_de_horario import garantir_horario_livre
from reservas.domain.excecoes import ReservaNaoEncontrada
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva
from reservas.domain.solicitante import Solicitante


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
        reserva = Reserva.solicitar(
            espaco_id=espaco_id,
            solicitante=solicitante,
            data=data,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim,
            finalidade=finalidade,
            agora=self._relogio(),
        )
        self._consulta_de_espacos.obter_espaco_reservavel(reserva.espaco_id)
        existentes = self._repositorio.listar_que_ocupam_horario(
            reserva.espaco_id, reserva.intervalo.data
        )
        garantir_horario_livre(reserva, existentes)
        return self._repositorio.salvar(reserva)


class ConsultarReservas:
    def __init__(self, repositorio: RepositorioReservas) -> None:
        self._repositorio = repositorio

    def executar(self, filtros: FiltrosDeReservas, *, ator: Ator) -> list[Reserva]:
        return self._repositorio.listar(_restringir_ao_ator(filtros, ator))


class ObterReserva:
    def __init__(self, repositorio: RepositorioReservas) -> None:
        self._repositorio = repositorio

    def executar(self, reserva_id: int, *, ator: Ator) -> Reserva:
        return _obter_ou_falhar(self._repositorio, reserva_id, ator)


class AlterarSituacaoReserva:
    def __init__(self, repositorio: RepositorioReservas) -> None:
        self._repositorio = repositorio

    def executar(
        self,
        *,
        reserva_id: int,
        nova_situacao: SituacaoReserva | str,
        motivo: str | None = None,
        ator: Ator,
    ) -> Reserva:
        reserva = _obter_ou_falhar(self._repositorio, reserva_id, ator)
        reserva.alterar_situacao(nova_situacao, motivo=motivo, ator=ator)
        return self._repositorio.salvar(reserva)


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
