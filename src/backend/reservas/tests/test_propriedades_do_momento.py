from datetime import timedelta

from hypothesis import given
from hypothesis import strategies as st

from reservas.domain.excecoes import ConclusaoAntesDoTermino, MudancaAposOInicio
from reservas.domain.situacao import SituacaoReserva as S
from reservas.tests.fakes import GESTOR, MOTIVO, intervalo, reserva_reconstituida

_HORAS = st.integers(min_value=7, max_value=20)
_MINUTOS = st.integers(min_value=0, max_value=59)
_DESLOCAMENTO = st.integers(min_value=-10 * 86400, max_value=10 * 86400)


@st.composite
def _reserva_e_instante(draw, situacao):
    hora = draw(_HORAS)
    inicio = f"{hora:02d}:{draw(_MINUTOS):02d}"
    fim = f"{hora + 1:02d}:{draw(_MINUTOS):02d}"
    if fim <= inicio:
        fim = f"{hora + 2:02d}:00"
    reserva = reserva_reconstituida(situacao=situacao, intervalo=intervalo(inicio, fim))
    agora = reserva.intervalo.inicio() + timedelta(seconds=draw(_DESLOCAMENTO))
    return reserva, agora


@given(_reserva_e_instante(S.CONFIRMADA))
def test_gestor_so_conclui_se_agora_e_no_minimo_o_termino(caso):
    # Arrange
    reserva, agora = caso
    termino = reserva.intervalo.fim()

    # Act
    oferecida = S.CONCLUIDA in reserva.acoes_permitidas_para(GESTOR, agora)
    try:
        reserva.alterar_situacao(S.CONCLUIDA, ator=GESTOR, agora=agora)
        aceita = True
    except ConclusaoAntesDoTermino:
        aceita = False

    # Assert
    assert aceita is (agora >= termino)
    assert oferecida is aceita


@given(
    _reserva_e_instante(S.SOLICITADA),
    st.sampled_from([S.RECUSADA, S.CANCELADA]),
)
def test_gestor_so_recusa_ou_cancela_se_agora_e_antes_do_inicio(caso, destino):
    # Arrange
    reserva, agora = caso
    inicio = reserva.intervalo.inicio()

    # Act
    oferecida = destino in reserva.acoes_permitidas_para(GESTOR, agora)
    try:
        reserva.alterar_situacao(destino, motivo=MOTIVO, ator=GESTOR, agora=agora)
        aceita = True
    except MudancaAposOInicio:
        aceita = False

    # Assert
    assert aceita is (agora < inicio)
    assert oferecida is aceita
