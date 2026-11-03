from datetime import datetime, timedelta

from hypothesis import given
from hypothesis import strategies as st

from compartilhado.domain.erros import ErroDeDominio
from reservas.domain.conflito_de_horario import garantir_horario_livre
from reservas.domain.excecoes import (
    AntecedenciaExcedida,
    DataRetroativa,
    DuracaoInvalida,
    ForaDoHorarioDeFuncionamento,
)
from reservas.domain.intervalo_de_horario import FUSO_HORARIO, IntervaloDeHorario
from reservas.domain.regras_de_agenda import (
    DURACAO_MAXIMA,
    DURACAO_MINIMA,
    GRANULARIDADE_DOS_HORARIOS_LIVRES,
    HORARIO_DE_ABERTURA,
    HORARIO_DE_FECHAMENTO,
    data_limite_para_reservar,
    horarios_livres,
    motivo_de_indisponibilidade,
)
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.estrategias import (
    ULTIMO_MINUTO_DO_DIA,
    hora,
    minutos,
    momentos_do_dia,
)
from reservas.tests.fakes import AGORA, reserva_reconstituida, reserva_solicitada

HOJE = AGORA.date()
_MINUTOS_DE_FOLGA_NAS_PONTAS = 2 * 60


def _duracao(intervalo):
    return intervalo.fim() - intervalo.inicio()


def _retroativa(intervalo, agora):
    return intervalo.inicio() <= agora


def _fora_do_funcionamento(intervalo, agora):
    return (
        intervalo.hora_inicio < HORARIO_DE_ABERTURA
        or intervalo.hora_fim > HORARIO_DE_FECHAMENTO
    )


def _duracao_fora_dos_limites(intervalo, agora):
    return not DURACAO_MINIMA <= _duracao(intervalo) <= DURACAO_MAXIMA


def _alem_da_antecedencia(intervalo, agora):
    return intervalo.data > data_limite_para_reservar(agora)


REGRAS_NA_ORDEM = [
    (DataRetroativa, _retroativa),
    (ForaDoHorarioDeFuncionamento, _fora_do_funcionamento),
    (DuracaoInvalida, _duracao_fora_dos_limites),
    (AntecedenciaExcedida, _alem_da_antecedencia),
]
_EXCECOES_DE_AGENDA = tuple(excecao for excecao, _ in REGRAS_NA_ORDEM)


@st.composite
def _pedidos(draw):
    data = HOJE + timedelta(days=draw(st.integers(-1, 32)))
    abertura, fechamento = minutos(HORARIO_DE_ABERTURA), minutos(HORARIO_DE_FECHAMENTO)
    inicio = draw(st.integers(abertura - _MINUTOS_DE_FOLGA_NAS_PONTAS, fechamento - 1))
    maior_fim = min(inicio + 4 * 60, ULTIMO_MINUTO_DO_DIA)
    fim = draw(st.integers(inicio + 1, maior_fim))
    intervalo = IntervaloDeHorario(
        data=data, hora_inicio=hora(inicio), hora_fim=hora(fim)
    )
    return intervalo, draw(momentos_do_dia(HOJE))


@given(pedido=_pedidos())
def test_solicitar_aceita_so_o_que_respeita_as_regras_e_recusa_pela_primeira_violada(
    pedido,
):
    # Arrange
    intervalo, agora = pedido

    # Act
    try:
        reserva_solicitada(
            data=intervalo.data,
            hora_inicio=intervalo.hora_inicio,
            hora_fim=intervalo.hora_fim,
            agora=agora,
        )
        recusa = None
    except _EXCECOES_DE_AGENDA as erro:
        recusa = type(erro)

    # Assert
    violadas = [
        excecao for excecao, violada in REGRAS_NA_ORDEM if violada(intervalo, agora)
    ]
    assert recusa == (violadas[0] if violadas else None)


@st.composite
def _ocupados_sem_sobreposicao(draw, data):
    pontos = sorted(
        draw(st.lists(st.integers(5 * 60, ULTIMO_MINUTO_DO_DIA), max_size=10))
    )
    ocupados = [
        IntervaloDeHorario(data=data, hora_inicio=hora(inicio), hora_fim=hora(fim))
        for inicio, fim in zip(pontos[::2], pontos[1::2], strict=False)
        if inicio < fim
    ]
    return draw(st.permutations(ocupados))


@st.composite
def _agendas(draw):
    data = HOJE + timedelta(days=draw(st.sampled_from([-1, 0, 0, 0, 1, 5])))
    return data, draw(momentos_do_dia(HOJE)), draw(_ocupados_sem_sobreposicao(data))


@given(agenda=_agendas())
def test_horarios_livres_sao_janelas_ordenadas_e_disjuntas_dentro_do_funcionamento(
    agenda,
):
    # Arrange
    data, agora, ocupados = agenda

    # Act
    livres = horarios_livres(ocupados, data=data, agora=agora)

    # Assert
    for anterior, seguinte in zip(livres, livres[1:], strict=False):
        assert anterior.fim() < seguinte.inicio()
    for livre in livres:
        assert livre.data == data
        assert livre.hora_inicio >= HORARIO_DE_ABERTURA
        assert livre.hora_fim <= HORARIO_DE_FECHAMENTO
        assert _duracao(livre) >= DURACAO_MINIMA
        assert livre.inicio() > agora
        assert not any(livre.sobrepoe(ocupado) for ocupado in ocupados)


def _aceita_pelo_backend(data, inicio, agora, ocupados):
    fim = (datetime.combine(data, inicio) + DURACAO_MINIMA).time()
    try:
        nova = reserva_solicitada(
            data=data, hora_inicio=inicio, hora_fim=fim, agora=agora
        )
        garantir_horario_livre(nova, ocupados)
    except ErroDeDominio:
        return False
    return True


def _cabe_numa_janela(data, inicio, livres):
    candidato_inicio = datetime.combine(data, inicio, tzinfo=FUSO_HORARIO)
    candidato_fim = candidato_inicio + DURACAO_MINIMA
    return any(
        livre.inicio() <= candidato_inicio and candidato_fim <= livre.fim()
        for livre in livres
    )


def _inicios_candidatos():
    passo = GRANULARIDADE_DOS_HORARIOS_LIVRES // timedelta(minutes=1)
    ultimo = minutos(HORARIO_DE_FECHAMENTO) - DURACAO_MINIMA // timedelta(minutes=1)
    return [hora(m) for m in range(minutos(HORARIO_DE_ABERTURA), ultimo + 1, passo)]


@given(agenda=_agendas())
def test_agenda_mostra_livre_exatamente_o_que_o_backend_aceitaria(agenda):
    # Arrange
    data, agora, ocupados = agenda
    reservas = [
        reserva_reconstituida(
            id=posicao, intervalo=ocupado, situacao=SituacaoReserva.CONFIRMADA
        )
        for posicao, ocupado in enumerate(ocupados, start=1)
    ]
    reservavel = motivo_de_indisponibilidade(data, agora) is None

    # Act
    livres = horarios_livres(ocupados, data=data, agora=agora)

    # Assert
    for inicio in _inicios_candidatos():
        aceita = _aceita_pelo_backend(data, inicio, agora, reservas)
        assert aceita is (reservavel and _cabe_numa_janela(data, inicio, livres)), (
            inicio
        )
