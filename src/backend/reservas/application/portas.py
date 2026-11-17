from dataclasses import dataclass
from typing import Protocol

from reservas.domain.funcionamento import FuncionamentoDoEspaco


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
