from datetime import timedelta

from espacos.domain.horario_de_funcionamento import JANELA_MINIMA_EM_MINUTOS
from reservas.domain.regras_de_agenda import DURACAO_MINIMA


def test_janela_minima_do_espaco_e_a_duracao_minima_da_reserva():
    assert timedelta(minutes=JANELA_MINIMA_EM_MINUTOS) == DURACAO_MINIMA
