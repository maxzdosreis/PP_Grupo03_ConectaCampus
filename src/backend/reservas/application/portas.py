from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import date, datetime
from typing import Protocol

from reservas.application.ocupacao_do_dia import HorarioOcupado
from reservas.domain.funcionamento import FuncionamentoDoEspaco
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.situacao import SituacaoReserva


@dataclass(frozen=True)
class EspacoReservavel:
    id: int
    nome: str
    funcionamento: FuncionamentoDoEspaco


class ConsultaDeEspacos(Protocol):
    def obter_espaco_reservavel(self, espaco_id: int) -> EspacoReservavel:
        """Devolve o espaço se ele existe e está ativo.

        Espaço inexistente lança um RecursoNaoEncontrado; inativo, um
        ConflitoDeEstado. Os erros sobem sem tradução.
        """

    def obter_espaco_reservavel_travado(self, espaco_id: int) -> EspacoReservavel:
        """Como `obter_espaco_reservavel`, mas trava o espaço até o fim da transação.

        Só pode ser chamada dentro de `RepositorioReservas.em_transacao`. A trava
        impede que o horário do espaço mude entre a leitura e a gravação da
        reserva (ESP-08); criações no mesmo espaço passam uma de cada vez.
        """

    def nomes_dos_espacos(self, ids: Iterable[int]) -> Mapping[int, str]:
        """Nome de cada espaço pedido, inclusive os inativos (só leitura).

        Id sem espaço fica de fora, sem erro; quem chama escolhe o que mostrar.
        """


class AgendaIndisponivel(Exception):
    """A projeção da agenda não pôde ser lida ou gravada.

    Não é erro de domínio e nunca deve chegar à API: quem chama cai para o
    PostgreSQL (leitura) ou só registra no log (escrita).
    """


class AgendaDoDia(Protocol):
    """Projeção da agenda de cada espaço e dia, reconstruível do PostgreSQL.

    Nunca decide conflito de horário (DEC-28). Uma operação com a projeção
    fora do ar lança `AgendaIndisponivel`.
    """

    def registrar(
        self,
        espaco_id: int,
        reserva_id: int,
        intervalo: IntervaloDeHorario,
        situacao: SituacaoReserva,
    ) -> None:
        """Grava ou atualiza a reserva na agenda do dia `intervalo.data`.

        Sem projeção desse espaço e dia, não grava nada (uma agenda parcial seria
        lida como completa), mas avança a `versao` do dia. Situação que não
        ocupa horário lança `ValueError`.
        """

    def remover(self, espaco_id: int, reserva_id: int, data: date) -> None:
        """Tira a reserva da agenda do dia. Idempotente.

        Sem projeção, não grava nada, mas avança a `versao` do dia.
        """

    def listar(self, espaco_id: int, data: date) -> tuple[HorarioOcupado, ...] | None:
        """Horários ocupados do dia, ordenados por início.

        Devolve `None` quando a projeção não existe (miss) e `()` para um dia
        sem reservas.
        """

    def dias_projetados(self, a_partir_de: date) -> frozenset[tuple[int, date]]:
        """Pares (espaço, data) com projeção existente e data >= `a_partir_de`.

        Inclui os dias vazios (só o sentinela). Só leitura.
        """

    def versao(self, espaco_id: int, data: date) -> int:
        """Contador do dia, que `registrar` e `remover` avançam a cada chamada.

        Leia-o **antes** de consultar o PostgreSQL e passe-o a `substituir`.
        """

    def substituir(
        self,
        espaco_id: int,
        data: date,
        ocupados: Mapping[int, HorarioOcupado],
        *,
        versao: int,
    ) -> bool:
        """Recria a projeção do dia a partir do que está no PostgreSQL.

        `ocupados` liga o id de cada reserva ao seu horário: o id faz parte do
        membro, para `registrar` e `remover` acharem a reserva depois.

        Só grava se a `versao` do dia ainda for a lida antes da consulta; senão
        alguém registrou ou removeu no meio e o retrato está velho. Devolve
        `True` se gravou e `False` se descartou (a próxima leitura refaz).
        """


class IndiceIndisponivel(Exception):
    """O índice de filas e contagens não pôde ser lido ou gravado.

    Independente de `AgendaIndisponivel`: as duas projeções falham sozinhas.
    Nunca chega à API; quem lê cai para o PostgreSQL e quem escreve só registra
    no log.
    """


@dataclass(frozen=True)
class RegistroDoIndice:
    reserva_id: int
    situacao: SituacaoReserva
    criada_em: datetime


def validar_janela(limite: int, deslocamento: int) -> None:
    if limite <= 0:
        raise ValueError("O limite deve ser maior que zero.")
    if deslocamento < 0:
        raise ValueError("O deslocamento não pode ser negativo.")


class IndiceDeReservas(Protocol):
    """Projeção da fila de pendentes e da contagem por situação.

    Reconstruível do PostgreSQL e nunca decide nada (DEC-28). Uma operação com
    a projeção fora do ar lança `IndiceIndisponivel`.
    """

    def aplicar(
        self, reserva_id: int, situacao: SituacaoReserva, criada_em: datetime
    ) -> None:
        """Põe a reserva na situação dada, tirando-a das outras e da fila.

        Por estado, não por transição: idempotente e imune à ordem das chamadas.
        Sem o índice montado, não grava nada, mas avança a `versao` (uma
        projeção parcial seria lida como completa).
        """

    def pendentes(self, limite: int, deslocamento: int = 0) -> tuple[int, ...] | None:
        """Ids das reservas Solicitadas, da mais antiga para a mais nova.

        `None` se o índice não está montado (miss); `()` se montado e vazio.
        Limite <= 0 ou deslocamento < 0 lança `ValueError`.
        """

    def contagem_por_situacao(self) -> dict[SituacaoReserva, int] | None:
        """Quantas reservas há em cada uma das situações (zero quando vazia).

        `None` se o índice não está montado.
        """

    def versao(self) -> int:
        """Contador que `aplicar` avança a cada chamada, montado ou não.

        Leia-o **antes** de consultar o PostgreSQL e passe-o a `substituir`.
        """

    def substituir(self, registros: Iterable[RegistroDoIndice], *, versao: int) -> bool:
        """Recria o índice inteiro a partir do que está no PostgreSQL.

        A troca é atômica e só acontece se a `versao` ainda for a lida antes da
        consulta; senão devolve `False` e nada muda. Falha no meio não deixa
        o índice pela metade.
        """


class RankingIndisponivel(Exception):
    """O ranking de espaços não pôde ser lido ou gravado.

    Independente de `AgendaIndisponivel` e de `IndiceIndisponivel`: as três
    projeções falham sozinhas. Nunca chega à API; quem lê cai para o PostgreSQL
    e quem escreve só registra no log.
    """


@dataclass(frozen=True)
class RegistroDoRanking:
    reserva_id: int
    espaco_id: int
    situacao: SituacaoReserva


class RankingDeEspacos(Protocol):
    """Projeção do total de reservas que contam, por espaço (RDS-12).

    Reconstruível do PostgreSQL e nunca decide nada (DEC-28). Uma operação com
    a projeção fora do ar lança `RankingIndisponivel`.
    """

    def aplicar(
        self, reserva_id: int, espaco_id: int, situacao: SituacaoReserva
    ) -> None:
        """Faz a reserva contar ou deixar de contar, conforme a situação.

        Por estado, não por evento: a reserva conta no máximo uma vez, e repetir,
        atrasar ou trocar a ordem das chamadas termina no estado da última
        aplicada. Sem o ranking montado, não grava nada, mas avança a `versao`.
        """

    def top(self, limite: int) -> tuple[tuple[int, int], ...] | None:
        """Pares (espaço, total) em ordem de total decrescente e, no empate, de
        id do espaço crescente. Espaços com total zero não aparecem.

        `None` se o ranking não está montado (miss); `()` se montado e vazio.
        Limite <= 0 lança `ValueError`.
        """

    def versao(self) -> int:
        """Contador que `aplicar` avança a cada chamada, montado ou não.

        Leia-o **antes** de consultar o PostgreSQL e passe-o a `substituir`.
        """

    def substituir(
        self, registros: Iterable[RegistroDoRanking], *, versao: int
    ) -> bool:
        """Recria o ranking inteiro a partir do que está no PostgreSQL.

        Só as reservas cuja situação conta entram. A troca é atômica e só
        acontece se a `versao` ainda for a lida antes da consulta; senão devolve
        `False` e nada muda.
        """
