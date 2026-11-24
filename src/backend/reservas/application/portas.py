from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
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
