from espacos import publico
from reservas.application.portas import ConsultaDeEspacos, EspacoReservavel


class ConsultaDeEspacosViaFachada(ConsultaDeEspacos):
    def obter_espaco_reservavel(self, espaco_id: int) -> EspacoReservavel:
        espaco = publico.verificar_espaco_disponivel(espaco_id)
        return EspacoReservavel(id=espaco.id, nome=espaco.nome)
