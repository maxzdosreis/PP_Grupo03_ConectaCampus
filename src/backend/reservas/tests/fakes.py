from collections.abc import Iterable

from compartilhado.domain.erros import ConflitoDeEstado, RecursoNaoEncontrado
from reservas.application.portas import ConsultaDeEspacos, EspacoReservavel


class ConsultaDeEspacosEmMemoria(ConsultaDeEspacos):
    def __init__(
        self,
        espacos: Iterable[EspacoReservavel] = (),
        *,
        ids_inativos: Iterable[int] = (),
    ) -> None:
        self._espacos = {espaco.id: espaco for espaco in espacos}
        self._ids_inativos = frozenset(ids_inativos)

    def obter_espaco_reservavel(self, espaco_id: int) -> EspacoReservavel:
        espaco = self._espacos.get(espaco_id)
        if espaco is None:
            raise RecursoNaoEncontrado(f"Espaço de código {espaco_id} não encontrado.")
        if espaco_id in self._ids_inativos:
            raise ConflitoDeEstado("Este espaço está inativo e não aceita reservas.")
        return espaco
