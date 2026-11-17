from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from reservas.domain.momento import exigir_fuso
from reservas.domain.situacao import SituacaoReserva

SITUACAO_PEDIDA_MAXIMO_CARACTERES = 20


class ResultadoDoRegistro(StrEnum):
    ACEITA = "ACEITA"
    RECUSADA = "RECUSADA"


@dataclass(frozen=True)
class RegistroDeSituacao:
    situacao_anterior: SituacaoReserva | None
    situacao_nova: SituacaoReserva
    motivo: str | None
    autor_usuario_id: int
    autor_nome: str
    registrado_em: datetime
    resultado: ResultadoDoRegistro = ResultadoDoRegistro.ACEITA
    codigo_do_erro: str | None = None
    situacao_pedida: str | None = None

    def __post_init__(self) -> None:
        _validar_situacoes(self.situacao_anterior, self.situacao_nova)
        recusada = self.resultado is ResultadoDoRegistro.RECUSADA
        if not recusada and self.situacao_anterior is self.situacao_nova:
            raise ValueError("situacao_anterior deve ser diferente de situacao_nova.")
        _validar_autor(self.autor_usuario_id, self.autor_nome)
        exigir_fuso(self.registrado_em, "registrado_em")
        if recusada:
            _validar_recusada(self)
        else:
            _validar_aceita(self)


def _validar_aceita(registro: RegistroDeSituacao) -> None:
    if registro.codigo_do_erro is not None:
        raise ValueError("Um registro aceito não tem codigo_do_erro.")
    if registro.situacao_pedida is None:
        object.__setattr__(registro, "situacao_pedida", registro.situacao_nova.value)
    elif registro.situacao_pedida != registro.situacao_nova.value:
        raise ValueError("Um registro aceito pede a própria situacao_nova.")


def _validar_recusada(registro: RegistroDeSituacao) -> None:
    if registro.situacao_anterior is not registro.situacao_nova:
        raise ValueError("Uma tentativa recusada não muda a situação da reserva.")
    if not registro.codigo_do_erro:
        raise ValueError("codigo_do_erro é obrigatório numa tentativa recusada.")
    pedida = registro.situacao_pedida
    if not isinstance(pedida, str) or not pedida:
        raise ValueError("situacao_pedida é obrigatória numa tentativa recusada.")
    if len(pedida) > SITUACAO_PEDIDA_MAXIMO_CARACTERES:
        raise ValueError(
            f"situacao_pedida deve ter até {SITUACAO_PEDIDA_MAXIMO_CARACTERES} "
            "caracteres."
        )


def _validar_situacoes(anterior: SituacaoReserva | None, nova: SituacaoReserva) -> None:
    if not isinstance(nova, SituacaoReserva):
        raise TypeError("situacao_nova deve ser uma SituacaoReserva.")
    if anterior is not None and not isinstance(anterior, SituacaoReserva):
        raise TypeError("situacao_anterior deve ser uma SituacaoReserva ou None.")


def _validar_autor(usuario_id: int, nome: str) -> None:
    if isinstance(usuario_id, bool) or not isinstance(usuario_id, int):
        raise ValueError("autor_usuario_id deve ser um inteiro positivo.")
    if usuario_id < 1:
        raise ValueError("autor_usuario_id deve ser um inteiro positivo.")
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("autor_nome é obrigatório.")
