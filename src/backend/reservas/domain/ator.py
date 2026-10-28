from dataclasses import dataclass
from enum import StrEnum


class PapelDoAtor(StrEnum):
    GESTOR = "GESTOR"
    SOLICITANTE = "SOLICITANTE"


@dataclass(frozen=True)
class Ator:

    usuario_id: int
    papel: PapelDoAtor
