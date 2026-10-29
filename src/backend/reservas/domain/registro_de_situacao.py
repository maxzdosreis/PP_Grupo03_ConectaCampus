from dataclasses import dataclass
from datetime import datetime

from reservas.domain.momento import exigir_fuso
from reservas.domain.situacao import SituacaoReserva


@dataclass(frozen=True)
class RegistroDeSituacao:
    situacao_anterior: SituacaoReserva | None
    situacao_nova: SituacaoReserva
    motivo: str | None
    autor_usuario_id: int
    autor_nome: str
    registrado_em: datetime

    def __post_init__(self) -> None:
        _validar_situacoes(self.situacao_anterior, self.situacao_nova)
        _validar_autor(self.autor_usuario_id, self.autor_nome)
        exigir_fuso(self.registrado_em, "registrado_em")


def _validar_situacoes(anterior: SituacaoReserva | None, nova: SituacaoReserva) -> None:
    if not isinstance(nova, SituacaoReserva):
        raise TypeError("situacao_nova deve ser uma SituacaoReserva.")
    if anterior is not None and not isinstance(anterior, SituacaoReserva):
        raise TypeError("situacao_anterior deve ser uma SituacaoReserva ou None.")
    if anterior is nova:
        raise ValueError("situacao_anterior deve ser diferente de situacao_nova.")


def _validar_autor(usuario_id: int, nome: str) -> None:
    if isinstance(usuario_id, bool) or not isinstance(usuario_id, int):
        raise ValueError("autor_usuario_id deve ser um inteiro positivo.")
    if usuario_id < 1:
        raise ValueError("autor_usuario_id deve ser um inteiro positivo.")
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("autor_nome é obrigatório.")
