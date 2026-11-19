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

    def obter_espaco_reservavel_travado(self, espaco_id: int) -> EspacoReservavel:
        """Como `obter_espaco_reservavel`, mas trava o espaço até o fim da transação.

        Só pode ser chamada dentro de `RepositorioReservas.em_transacao`. A trava
        impede que o horário do espaço mude entre a leitura e a gravação da
        reserva (ESP-08); criações no mesmo espaço passam uma de cada vez.
        """
