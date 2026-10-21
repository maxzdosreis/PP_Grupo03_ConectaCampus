from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class EspacoReservavel:
    id: int
    nome: str


class ConsultaDeEspacos(Protocol):
    def obter_espaco_reservavel(self, espaco_id: int) -> EspacoReservavel:

