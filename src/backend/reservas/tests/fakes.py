from collections.abc import Iterable
from datetime import date

from compartilhado.domain.erros import ConflitoDeEstado, RecursoNaoEncontrado
from reservas.application.portas import ConsultaDeEspacos, EspacoReservavel
from reservas.application.repositorio import FiltrosDeReservas, RepositorioReservas
from reservas.domain.conflito_de_horario import garantir_horario_livre
from reservas.domain.excecoes import ReservaNaoEncontrada
from reservas.domain.reserva import Reserva


class ConsultaDeEspacosEmMemoria(ConsultaDeEspacos):
    def __init__(
        self,
        espacos: Iterable[EspacoReservavel] = (),
        *,
        ids_inativos: Iterable[int] = (),
    ) -> None:
        self._espacos = {espaco.id: espaco for espaco in espacos}
        self._ids_inativos = frozenset(ids_inativos)

    def obter_espaco_reservavel(self, espaco_id: int) -> EspacoReservavel:
        espaco = self._espacos.get(espaco_id)
        if espaco is None:
            raise RecursoNaoEncontrado(f"Espaço de código {espaco_id} não encontrado.")
        if espaco_id in self._ids_inativos:
            raise ConflitoDeEstado("Este espaço está inativo e não aceita reservas.")
        return espaco


class RepositorioReservasEmMemoria(RepositorioReservas):
    def __init__(self) -> None:
        self._reservas: dict[int, Reserva] = {}
        self._proximo_id = 1

    def salvar(self, reserva: Reserva) -> Reserva:
        if reserva.id is not None and reserva.id not in self._reservas:
            raise ReservaNaoEncontrada(reserva.id)
        # Imita a exclusion constraint do banco, que só vale para quem ocupa horário.
        if reserva.situacao.ocupa_horario:
            garantir_horario_livre(reserva, self._reservas.values())
        reserva_id = reserva.id if reserva.id is not None else self._gerar_id()
        self._reservas[reserva_id] = _copiar(reserva, reserva_id)
        return _copiar(reserva, reserva_id)

    def obter_por_id(self, reserva_id: int) -> Reserva | None:
        reserva = self._reservas.get(reserva_id)
        return _copiar(reserva, reserva_id) if reserva else None

    def listar(self, filtros: FiltrosDeReservas) -> list[Reserva]:
        return self._ordenadas(
            reserva
            for reserva in self._reservas.values()
            if _atende_aos_filtros(reserva, filtros)
        )

    def listar_que_ocupam_horario(self, espaco_id: int, data: date) -> list[Reserva]:
        return self._ordenadas(
            reserva
            for reserva in self._reservas.values()
            if reserva.espaco_id == espaco_id
            and reserva.intervalo.data == data
            and reserva.situacao.ocupa_horario
        )

    def _ordenadas(self, reservas: Iterable[Reserva]) -> list[Reserva]:
        encontradas = sorted(
            reservas, key=lambda reserva: (reserva.intervalo.inicio(), reserva.id)
        )
        return [_copiar(reserva, reserva.id) for reserva in encontradas]

    def _gerar_id(self) -> int:
        reserva_id = self._proximo_id
        self._proximo_id += 1
        return reserva_id


def _atende_aos_filtros(reserva: Reserva, filtros: FiltrosDeReservas) -> bool:
    return (
        filtros.espaco_id in (None, reserva.espaco_id)
        and filtros.situacao in (None, reserva.situacao)
        and filtros.data in (None, reserva.intervalo.data)
        and filtros.solicitante_usuario_id in (None, reserva.solicitante.usuario_id)
        and _solicitante_contem(reserva, filtros.solicitante)
    )


def _solicitante_contem(reserva: Reserva, trecho: str | None) -> bool:
    if trecho is None:
        return True
    trecho = trecho.casefold()
    return (
        trecho in reserva.solicitante.nome.casefold()
        or trecho in reserva.solicitante.matricula.casefold()
    )


def _copiar(reserva: Reserva, reserva_id: int | None) -> Reserva:
    return Reserva(
        id=reserva_id,
        espaco_id=reserva.espaco_id,
        solicitante=reserva.solicitante,
        intervalo=reserva.intervalo,
        finalidade=reserva.finalidade,
        situacao=reserva.situacao,
        motivo_da_situacao=reserva.motivo_da_situacao,
        criada_em=reserva.criada_em,
    )
