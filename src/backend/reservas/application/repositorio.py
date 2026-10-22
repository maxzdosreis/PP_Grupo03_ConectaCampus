from dataclasses import dataclass
from datetime import date
from typing import Protocol

from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva


@dataclass(frozen=True)
class FiltrosDeReservas:
    espaco_id: int | None = None
    situacao: SituacaoReserva | None = None
    data: date | None = None
    solicitante_usuario_id: int | None = None
    solicitante: str | None = None


class RepositorioReservas(Protocol):
    def salvar(self, reserva: Reserva) -> Reserva:
        """Insere quando o id é None e atualiza quando já existe.

        Devolve a entidade com id. Atualizar um id inexistente lança
        ReservaNaoEncontrada; ocupar o horário de outra reserva do mesmo espaço
        lança ConflitoDeHorario.
        """

    def obter_por_id(self, reserva_id: int) -> Reserva | None:
        """Devolve a reserva ou None; o caso de uso decide se a ausência é erro."""

    def listar(self, filtros: FiltrosDeReservas) -> list[Reserva]:
        """Lista as reservas por início e, no empate, por id.

        Os filtros informados se somam. solicitante busca um trecho do nome ou da
        matrícula, sem diferenciar maiúsculas.
        """

    def listar_que_ocupam_horario(self, espaco_id: int, data: date) -> list[Reserva]:
        """Lista as reservas Solicitadas ou Confirmadas do espaço naquele dia."""
