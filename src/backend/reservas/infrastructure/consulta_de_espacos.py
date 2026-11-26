from collections.abc import Iterable, Mapping

from espacos import publico
from reservas.application.portas import ConsultaDeEspacos, EspacoReservavel
from reservas.domain.funcionamento import FuncionamentoDoEspaco


class ConsultaDeEspacosViaFachada(ConsultaDeEspacos):
    def obter_espaco_reservavel(self, espaco_id: int) -> EspacoReservavel:
        return _como_reservavel(publico.verificar_espaco_disponivel(espaco_id))

    def obter_espaco_reservavel_travado(self, espaco_id: int) -> EspacoReservavel:
        return _como_reservavel(
            publico.verificar_espaco_disponivel_para_reserva(espaco_id)
        )

    def nomes_dos_espacos(self, ids: Iterable[int]) -> Mapping[int, str]:
        return publico.nomes_dos_espacos(ids)


def _como_reservavel(espaco: publico.EspacoDisponivel) -> EspacoReservavel:
    return EspacoReservavel(
        id=espaco.id,
        nome=espaco.nome,
        funcionamento=FuncionamentoDoEspaco(
            abertura_em_minutos=espaco.abertura_em_minutos,
            fechamento_em_minutos=espaco.fechamento_em_minutos,
        ),
    )
