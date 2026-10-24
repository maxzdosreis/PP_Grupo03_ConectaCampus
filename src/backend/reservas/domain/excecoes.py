from typing import TYPE_CHECKING

from compartilhado.domain.erros import (
    ConflitoDeEstado,
    DadosInvalidos,
    RecursoNaoEncontrado,
)
from reservas.domain.situacao import SituacaoReserva

if TYPE_CHECKING:
    from reservas.domain.intervalo_de_horario import IntervaloDeHorario

_SITUACOES_ACEITAS = ", ".join(situacao.rotulo for situacao in SituacaoReserva)


class IdentificadorDeEspacoInvalido(DadosInvalidos):
    codigo = "IDENTIFICADOR_DE_ESPACO_INVALIDO"
    campo = "espaco_id"
    mensagem_padrao = "O espaço deve ser informado por um número inteiro positivo."


class HorarioInvalido(DadosInvalidos):
    codigo = "HORARIO_INVALIDO"
    campo = "hora_fim"
    mensagem_padrao = "O horário de término deve ser posterior ao de início."


class DataRetroativa(DadosInvalidos):
    codigo = "DATA_RETROATIVA"
    campo = "data"
    mensagem_padrao = "Não é possível reservar um horário que já passou."


class SituacaoInvalida(DadosInvalidos):
    codigo = "SITUACAO_INVALIDA"
    campo = "situacao"
    mensagem_padrao = f"Situação inválida. Escolha uma destas: {_SITUACOES_ACEITAS}."


class MotivoObrigatorio(DadosInvalidos):
    codigo = "MOTIVO_OBRIGATORIO"
    campo = "motivo"
    mensagem_padrao = "Informe o motivo para recusar ou cancelar a reserva."


class TransicaoDeSituacaoInvalida(ConflitoDeEstado):
    codigo = "TRANSICAO_DE_SITUACAO_INVALIDA"

    def __init__(self, atual: SituacaoReserva, nova: SituacaoReserva) -> None:
        self.atual = atual
        self.nova = nova
        super().__init__(
            f"Não é possível alterar uma reserva {atual.rotulo} para {nova.rotulo}."
        )


class ConflitoDeHorario(ConflitoDeEstado):
    codigo = "CONFLITO_DE_HORARIO"

    def __init__(
        self, intervalo: "IntervaloDeHorario", situacao: SituacaoReserva
    ) -> None:
        self.intervalo = intervalo
        self.situacao = situacao
        super().__init__(
            f"Este espaço já tem uma reserva {situacao.rotulo} em {intervalo}. "
            "Escolha outro horário."
        )


class ReservaNaoEncontrada(RecursoNaoEncontrado):
    codigo = "RESERVA_NAO_ENCONTRADA"

    def __init__(self, reserva_id: int) -> None:
        self.reserva_id = reserva_id
        super().__init__(f"Reserva de código {reserva_id} não encontrada.")
