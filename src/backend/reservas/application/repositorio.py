from collections.abc import Sequence
from contextlib import AbstractContextManager
from dataclasses import dataclass
from datetime import date, datetime
from typing import Protocol

from reservas.application.portas import RegistroDoIndice
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
    def em_transacao(self) -> AbstractContextManager[None]:
        """Abre uma transação que vale até o fim do bloco `with` (ESP-08).

        Tudo o que o caso de uso lê e grava dentro dela, inclusive as travas
        tomadas por outras portas na mesma conexão, confirma ou desfaz junto.
        """

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

    def gravar_tentativa_recusada(
        self, reserva_id: int, registro: RegistroDeSituacao
    ) -> None:
        """Grava, numa transação própria e já confirmada, a tentativa recusada.

        Não toca na reserva: só acrescenta o registro ao histórico dela. A
        transação é independente de qualquer outra, para a recusa de uma mudança
        não desfazer o registro da tentativa (DEC-05). Id inexistente lança
        ReservaNaoEncontrada.
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

    def listar_pendentes(self, paginacao: Paginacao) -> PaginaDeReservas:
        """Devolve uma página das reservas Solicitadas, da mais antiga para a mais
        nova (`criada_em` e, no empate, id), na ordem da fila de pendentes.

        total conta todas as Solicitadas. Uma página depois da última vem sem
        itens, com o total certo. A paginação acontece na consulta.
        """

    def listar_por_ids(self, ids: Sequence[int]) -> list[Reserva]:
        """Devolve as reservas dos ids pedidos, de qualquer situação, na ordem dos ids.

        Ids inexistentes ficam de fora, sem erro. Ids repetidos devolvem uma só
        reserva. Quem pede decide o que fazer com as que não interessam.
        """

    def contar_por_situacao(self) -> dict[SituacaoReserva, int]:
        """Quantas reservas há em cada situação, na ordem de `SituacaoReserva`.

        Sempre traz as cinco situações, com zero quando não há nenhuma.
        """

    def listar_que_ocupam_horario(self, espaco_id: int, data: date) -> list[Reserva]:
        """Lista as reservas Solicitadas ou Confirmadas do espaço naquele dia."""

    def listar_dias_com_reservas_que_ocupam_horario(
        self, a_partir_de: date
    ) -> list[tuple[int, date]]:
        """Pares distintos (espaço, data de início) das reservas Solicitadas ou
        Confirmadas com data >= `a_partir_de`, ordenados por espaço e data."""

    def listar_ativas_a_partir_de(
        self, espaco_id: int, momento: datetime
    ) -> list[Reserva]:
        """Lista as reservas Solicitadas ou Confirmadas do espaço que terminam
        depois do momento (as futuras e a que está em andamento), por início."""

    def listar_historico(self, reserva_id: int) -> list[RegistroDeSituacao]:
        """Lista o histórico da reserva por registrado_em e, no empate, na ordem
        em que os registros foram gravados. Id inexistente devolve lista vazia.
        """

    def listar_para_indice(
        self, depois_de_id: int, limite: int
    ) -> list[RegistroDoIndice]:
        """Até `limite` reservas com id maior que `depois_de_id`, por id.

        Só id, situação e criada_em, para a reconstrução do índice ler em lotes
        sem trazer a tabela inteira nem o histórico.
        """
