from datetime import date, datetime, time, timedelta

from hypothesis import strategies as st

from reservas.domain.funcionamento import FuncionamentoDoEspaco
from reservas.domain.intervalo_de_horario import FUSO_HORARIO, IntervaloDeHorario
from reservas.domain.solicitante import Solicitante
from reservas.tests.fakes import DIA, UTC

MINUTOS_POR_HORA = 60
ULTIMO_MINUTO_DO_DIA = 24 * MINUTOS_POR_HORA - 1
MINUTOS_NO_DIA = 24 * MINUTOS_POR_HORA
JANELA_MINIMA = 30
SO_O_DIA_PADRAO = st.just(DIA)


def hora(minutos: int) -> time:
    return time(*divmod(minutos, MINUTOS_POR_HORA))


def minutos(horario: time) -> int:
    return horario.hour * MINUTOS_POR_HORA + horario.minute


def hora_do_termino(minutos_do_dia: int) -> time:
    """1440 (fim do dia) é escrito 00:00; os demais valores são horas comuns."""
    return hora(minutos_do_dia % MINUTOS_NO_DIA)


def minutos_do_termino(horario: time) -> int:
    """Oráculo independente dos datetimes: 00:00 como término vale 1440."""
    return minutos(horario) or MINUTOS_NO_DIA


@st.composite
def funcionamentos(draw) -> FuncionamentoDoEspaco:
    """Qualquer janela válida de um espaço, inclusive as que fecham à meia-noite."""
    abertura = draw(st.integers(0, MINUTOS_NO_DIA - JANELA_MINIMA))
    fechamento = draw(
        st.one_of(
            st.just(MINUTOS_NO_DIA),
            st.integers(abertura + JANELA_MINIMA, MINUTOS_NO_DIA),
        )
    )
    return FuncionamentoDoEspaco(abertura, fechamento)


@st.composite
def intervalos(
    draw,
    *,
    datas=SO_O_DIA_PADRAO,
    de: int = 0,
    ate: int = ULTIMO_MINUTO_DO_DIA,
) -> IntervaloDeHorario:
    inicio = draw(st.integers(de, ate - 1))
    fim = draw(st.integers(inicio + 1, ate))
    return IntervaloDeHorario(
        data=draw(datas), hora_inicio=hora(inicio), hora_fim=hora(fim)
    )


def em_sao_paulo_ou_utc(momento: datetime):
    return st.sampled_from([momento, momento.astimezone(UTC)])


@st.composite
def momentos_do_dia(draw, dia: date) -> datetime:
    segundos = draw(st.integers(0, 24 * 60 * 60 - 1))
    momento = datetime.combine(dia, time(), tzinfo=FUSO_HORARIO)
    return draw(em_sao_paulo_ou_utc(momento + timedelta(seconds=segundos)))


_LETRA = st.characters(categories=("L",))

solicitantes = st.builds(
    Solicitante,
    usuario_id=st.integers(min_value=1, max_value=10**6),
    nome=st.text(_LETRA, min_size=1, max_size=20),
    matricula=st.from_regex(r"\A[0-9]{7}\Z"),
)
