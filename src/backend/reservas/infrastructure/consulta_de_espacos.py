from espacos import publico
from reservas.application.portas import ConsultaDeEspacos, EspacoReservavel
from reservas.domain.funcionamento import FuncionamentoDoEspaco


class ConsultaDeEspacosViaFachada(ConsultaDeEspacos):
    def obter_espaco_reservavel(self, espaco_id: int) -> EspacoReservavel:
        espaco = publico.verificar_espaco_disponivel(espaco_id)
        return EspacoReservavel(
            id=espaco.id,
            nome=espaco.nome,
            funcionamento=FuncionamentoDoEspaco(
                abertura_em_minutos=espaco.abertura_em_minutos,
                fechamento_em_minutos=espaco.fechamento_em_minutos,
            ),
        )
