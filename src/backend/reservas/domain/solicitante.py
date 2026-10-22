from dataclasses import dataclass

from compartilhado.domain.erros import CampoObrigatorioAusente
from reservas.domain.texto import normalizar_espacos


@dataclass(frozen=True)
class Solicitante:
    usuario_id: int
    nome: str
    matricula: str

    def __post_init__(self) -> None:
        _validar_usuario_id(self.usuario_id)
        object.__setattr__(self, "nome", _normalizar_nome(self.nome))
        object.__setattr__(self, "matricula", _normalizar_matricula(self.matricula))


def _validar_usuario_id(usuario_id: int | None) -> None:
    if usuario_id is None:
        raise CampoObrigatorioAusente("usuario_id", "Usuário")
    if isinstance(usuario_id, bool) or not isinstance(usuario_id, int):
        raise ValueError("usuario_id deve ser um inteiro positivo.")
    if usuario_id < 1:
        raise ValueError("usuario_id deve ser um inteiro positivo.")


def _normalizar_nome(nome: str | None) -> str:
    nome_normalizado = normalizar_espacos(nome)
    if not nome_normalizado:
        raise CampoObrigatorioAusente("nome", "Nome")
    return nome_normalizado


def _normalizar_matricula(matricula: str | None) -> str:
    matricula_normalizada = (matricula or "").strip()
    if not matricula_normalizada:
        raise CampoObrigatorioAusente("matricula", "Matrícula")
    return matricula_normalizada
