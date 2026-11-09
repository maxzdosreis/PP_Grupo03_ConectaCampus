from dataclasses import dataclass
from datetime import date
from typing import Protocol

from reservas.domain.registro_de_situacao import RegistroDeSituacao
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva

TAMANHO_PADRAO_DA_PAGINA = 20
TAMANHO_MAXIMO_DA_PAGINA = 100


@dataclass(frozen=True)
class FiltrosDeReservas:
    espaco_id: int | None = None
    situacao: SituacaoReserva | None = None
    data: date | None = None
    solicitante_usuario_id: int | None = None
    solicitante: str | None = None


@dataclass(frozen=True)
class Paginacao:
    numero: int = 1
    tamanho: int = TAMANHO_PADRAO_DA_PAGINA

    def __post_init__(self) -> None:
        _exigir_inteiro("numero", self.numero)
        _exigir_inteiro("tamanho", self.tamanho)
        if self.numero < 1:
            raise ValueError("O número da página deve ser 1 ou maior.")
        if not 1 <= self.tamanho <= TAMANHO_MAXIMO_DA_PAGINA:
            raise ValueError(
                f"O tamanho da página deve ficar entre 1 e {TAMANHO_MAXIMO_DA_PAGINA}."
            )

    def deslocamento(self) -> int:
        return (self.numero - 1) * self.tamanho


@dataclass(frozen=True)
class PaginaDeReservas:
    itens: tuple[Reserva, ...]
    total: int
    paginacao: Paginacao

    def total_de_paginas(self) -> int:
        return -(-self.total // self.paginacao.tamanho)


def _exigir_inteiro(nome: str, valor: object) -> None:
    if not isinstance(valor, int) or isinstance(valor, bool):
        raise TypeError(f"{nome} da paginação deve ser int, recebido {valor!r}.")


class RepositorioReservas(Protocol):
    def salvar(self, reserva: Reserva) -> Reserva:
        """Insere quando o id é None e atualiza quando já existe.

        Grava também os registros_pendentes da reserva no histórico, na mesma
        transação: se a gravação falhar, nem a reserva nem os registros ficam
        gravados. Depois do sucesso, a entidade recebida fica sem pendentes, para
        salvar de novo não duplicar o histórico.

        Atualizar uma reserva cuja situação gravada não é mais a
        situacao_de_origem (alterada por outra operação depois da leitura) lança
        ReservaDesatualizada, sem gravar nada.

        Devolve a entidade com id. Atualizar um id inexistente lança
        ReservaNaoEncontrada; ocupar o horário de outra reserva do mesmo espaço
        lança ConflitoDeHorario.
        """

    def obter_por_id(self, reserva_id: int) -> Reserva | None:
        """Devolve a reserva ou None; o caso de uso decide se a ausência é erro."""

    def listar(
        self, filtros: FiltrosDeReservas, paginacao: Paginacao
    ) -> PaginaDeReservas:
        """Devolve uma página das reservas, ordenadas por início e, no empate, por id.

        Os filtros informados se somam. solicitante busca um trecho do nome ou da
        matrícula, sem diferenciar maiúsculas. total conta todas as reservas que
        atendem aos filtros, não só as da página. A ordem é estável: concatenar as
        páginas 1 a total_de_paginas(), em ordem, dá a lista completa, sem
        repetição. Uma página depois da última vem sem itens, com o total certo.
        A paginação acontece na consulta, sem carregar as demais reservas.
        """

    def listar_que_ocupam_horario(self, espaco_id: int, data: date) -> list[Reserva]:
        """Lista as reservas Solicitadas ou Confirmadas do espaço naquele dia."""

    def listar_historico(self, reserva_id: int) -> list[RegistroDeSituacao]:
        """Lista o histórico da reserva por registrado_em e, no empate, na ordem
        em que os registros foram gravados. Id inexistente devolve lista vazia.
        """
