from datetime import date, time, timedelta
from typing import TYPE_CHECKING

from compartilhado.domain.erros import (
    AcaoNaoPermitida,
    ConflitoDeEstado,
    DadosInvalidos,
    RecursoNaoEncontrado,
)
from reservas.domain.situacao import SituacaoReserva

if TYPE_CHECKING:
    from reservas.domain.intervalo_de_horario import IntervaloDeHorario

_SITUACOES_ACEITAS = ", ".join(situacao.rotulo for situacao in SituacaoReserva)
_MINUTOS_POR_HORA = 60


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


class ForaDoHorarioDeFuncionamento(DadosInvalidos):
    codigo = "FORA_DO_HORARIO_DE_FUNCIONAMENTO"

    def __init__(self, campo: str, abertura: time, fechamento: time) -> None:
        self.campo = campo
        super().__init__(
            f"Os espaços funcionam das {abertura:%H:%M} às {fechamento:%H:%M}. "
            "Escolha um horário dentro desse período."
        )


class DuracaoInvalida(DadosInvalidos):
    codigo = "DURACAO_INVALIDA"
    campo = "hora_fim"

    def __init__(self, minima: timedelta, maxima: timedelta) -> None:
        super().__init__(
            f"A reserva deve durar entre {_descrever_duracao(minima)} "
            f"e {_descrever_duracao(maxima)}."
        )


class AntecedenciaExcedida(DadosInvalidos):
    codigo = "ANTECEDENCIA_EXCEDIDA"
    campo = "data"

    def __init__(self, dias: int, data_limite: date) -> None:
        self.data_limite = data_limite
        super().__init__(
            f"Só é possível reservar com até {dias} dias de antecedência "
            f"(até {data_limite:%d/%m/%Y})."
        )


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


class ReservaDesatualizada(ConflitoDeEstado):
    codigo = "RESERVA_DESATUALIZADA"

    def __init__(self, situacao_atual: SituacaoReserva) -> None:
        self.situacao_atual = situacao_atual
        super().__init__(
            f"Esta reserva já está {situacao_atual.rotulo}: ela foi alterada "
            "enquanto você decidia. Atualize a lista e tente de novo."
        )


class AlteracaoDeSituacaoNaoPermitida(AcaoNaoPermitida):
    codigo = "ACAO_NAO_PERMITIDA"

    def __init__(self, nova: SituacaoReserva) -> None:
        self.nova = nova
        super().__init__(
            f"Somente o gestor pode {nova.rotulo_da_acao.lower()} reservas."
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


def _descrever_duracao(duracao: timedelta) -> str:
    horas, minutos = divmod(duracao // timedelta(minutes=1), _MINUTOS_POR_HORA)
    partes = [
        _quantidade(horas, "hora", "horas"),
        _quantidade(minutos, "minuto", "minutos"),
    ]
    return " e ".join(parte for parte in partes if parte)


def _quantidade(valor: int, singular: str, plural: str) -> str:
    if not valor:
        return ""
    return f"{valor} {singular if valor == 1 else plural}"
