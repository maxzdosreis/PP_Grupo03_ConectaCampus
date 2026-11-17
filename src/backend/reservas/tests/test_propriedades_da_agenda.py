from datetime import datetime, timedelta

import pytest
from hypothesis import given
from hypothesis import strategies as st

from compartilhado.domain.erros import ErroDeDominio
from reservas.domain.conflito_de_horario import garantir_horario_livre
from reservas.domain.excecoes import (
    AntecedenciaExcedida,
    DataRetroativa,
    DuracaoInvalida,
    ForaDoHorarioDeFuncionamento,
    HorarioInvalido,
)
from reservas.domain.intervalo_de_horario import FUSO_HORARIO, IntervaloDeHorario
from reservas.domain.regras_de_agenda import (
    DURACAO_MAXIMA,
    DURACAO_MINIMA,
    GRANULARIDADE_DOS_HORARIOS_LIVRES,
    data_limite_para_reservar,
    horarios_livres,
    motivo_de_indisponibilidade,
)
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.estrategias import (
    MINUTOS_NO_DIA,
    funcionamentos,
    hora,
    hora_do_termino,
    minutos,
    minutos_do_termino,
    momentos_do_dia,
)
from reservas.tests.fakes import AGORA, reserva_reconstituida, reserva_solicitada

HOJE = AGORA.date()
_MINUTOS_DE_FOLGA_NAS_PONTAS = 2 * 60


def _duracao(intervalo):
    return intervalo.fim() - intervalo.inicio()


def _retroativa(intervalo, agora, funcionamento):
    return intervalo.inicio() <= agora


def _fora_do_funcionamento(intervalo, agora, funcionamento):
    return (
        minutos(intervalo.hora_inicio) < funcionamento.abertura_em_minutos
        or minutos_do_termino(intervalo.hora_fim) > funcionamento.fechamento_em_minutos
    )


def _duracao_fora_dos_limites(intervalo, agora, funcionamento):
    duracao = minutos_do_termino(intervalo.hora_fim) - minutos(intervalo.hora_inicio)
    return not DURACAO_MINIMA <= timedelta(minutes=duracao) <= DURACAO_MAXIMA


def _alem_da_antecedencia(intervalo, agora, funcionamento):
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
    funcionamento = draw(funcionamentos())
    data = HOJE + timedelta(days=draw(st.integers(-1, 32)))
    inicio = draw(
        st.integers(
            max(funcionamento.abertura_em_minutos - _MINUTOS_DE_FOLGA_NAS_PONTAS, 0),
            min(funcionamento.fechamento_em_minutos + 1, MINUTOS_NO_DIA - 1),
        )
    )
    fim = draw(st.integers(inicio + 1, min(inicio + 4 * 60, MINUTOS_NO_DIA)))
    intervalo = IntervaloDeHorario(
        data=data, hora_inicio=hora(inicio), hora_fim=hora_do_termino(fim)
    )
    return intervalo, draw(momentos_do_dia(HOJE)), funcionamento


@given(pedido=_pedidos())
def test_solicitar_aceita_so_o_que_respeita_as_regras_e_recusa_pela_primeira_violada(
    pedido,
):
    # Arrange
    intervalo, agora, funcionamento = pedido

    # Act
    try:
        reserva_solicitada(
            data=intervalo.data,
            hora_inicio=intervalo.hora_inicio,
            hora_fim=intervalo.hora_fim,
            agora=agora,
            funcionamento=funcionamento,
        )
        recusa = None
    except _EXCECOES_DE_AGENDA as erro:
        recusa = type(erro)

    # Assert
    violadas = [
        excecao
        for excecao, violada in REGRAS_NA_ORDEM
        if violada(intervalo, agora, funcionamento)
    ]
    assert recusa == (violadas[0] if violadas else None)


@st.composite
def _ocupados_sem_sobreposicao(draw, data):
    pontos = sorted(draw(st.lists(st.integers(5 * 60, MINUTOS_NO_DIA), max_size=10)))
    ocupados = [
        IntervaloDeHorario(
            data=data, hora_inicio=hora(inicio), hora_fim=hora_do_termino(fim)
        )
        for inicio, fim in zip(pontos[::2], pontos[1::2], strict=False)
        if inicio < fim
    ]
    return draw(st.permutations(ocupados))


@st.composite
def _agendas(draw):
    data = HOJE + timedelta(days=draw(st.sampled_from([-1, 0, 0, 0, 1, 5])))
    return (
        data,
        draw(momentos_do_dia(HOJE)),
        draw(_ocupados_sem_sobreposicao(data)),
        draw(funcionamentos()),
    )


@given(agenda=_agendas())
def test_horarios_livres_sao_janelas_ordenadas_e_disjuntas_dentro_do_funcionamento(
    agenda,
):
    # Arrange
    data, agora, ocupados, funcionamento = agenda

    # Act
    livres = horarios_livres(
        ocupados, data=data, agora=agora, funcionamento=funcionamento
    )

    # Assert
    for anterior, seguinte in zip(livres, livres[1:], strict=False):
        assert anterior.fim() < seguinte.inicio()
    for livre in livres:
        assert livre.data == data
        assert minutos(livre.hora_inicio) >= funcionamento.abertura_em_minutos
        assert minutos_do_termino(livre.hora_fim) <= funcionamento.fechamento_em_minutos
        assert _duracao(livre) >= DURACAO_MINIMA
        assert livre.inicio() > agora
        assert not any(livre.sobrepoe(ocupado) for ocupado in ocupados)


def _aceita_pelo_backend(data, inicio, agora, ocupados, funcionamento):
    fim = (datetime.combine(data, inicio) + DURACAO_MINIMA).time()
    try:
        nova = reserva_solicitada(
            data=data,
            hora_inicio=inicio,
            hora_fim=fim,
            agora=agora,
            funcionamento=funcionamento,
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


def _inicios_candidatos(funcionamento):
    # A agenda oferece inícios na grade de 5 minutos (decisão c da FE-07); a abertura
    # de um espaço pode cair fora dela (a agenda a mostra como veio do cadastro).
    passo = GRANULARIDADE_DOS_HORARIOS_LIVRES // timedelta(minutes=1)
    ultimo = funcionamento.fechamento_em_minutos - DURACAO_MINIMA // timedelta(
        minutes=1
    )
    primeiro = -(-funcionamento.abertura_em_minutos // passo) * passo
    return [hora(m) for m in range(primeiro, ultimo + 1, passo)]


@given(agenda=_agendas())
def test_agenda_mostra_livre_exatamente_o_que_o_backend_aceitaria(agenda):
    # Arrange
    data, agora, ocupados, funcionamento = agenda
    reservas = [
        reserva_reconstituida(
            id=posicao, intervalo=ocupado, situacao=SituacaoReserva.CONFIRMADA
        )
        for posicao, ocupado in enumerate(ocupados, start=1)
    ]
    reservavel = motivo_de_indisponibilidade(data, agora, funcionamento) is None

    # Act
    livres = horarios_livres(
        ocupados, data=data, agora=agora, funcionamento=funcionamento
    )

    # Assert
    for inicio in _inicios_candidatos(funcionamento):
        aceita = _aceita_pelo_backend(data, inicio, agora, reservas, funcionamento)
        assert aceita is (reservavel and _cabe_numa_janela(data, inicio, livres)), (
            inicio
        )


@given(
    funcionamento=funcionamentos(), data=st.sampled_from([HOJE, HOJE + timedelta(5)])
)
def test_fechar_a_00_00_equivale_a_fechar_a_24_00(funcionamento, data):
    # Arrange
    fechamento_a_meia_noite = funcionamento.fechamento_em_minutos == MINUTOS_NO_DIA

    # Assert
    assert (funcionamento.fechamento() == hora(0)) is fechamento_a_meia_noite
    if fechamento_a_meia_noite:
        assert funcionamento.fecha_em(data) == datetime.combine(
            data + timedelta(days=1), hora(0), tzinfo=FUSO_HORARIO
        )


@given(
    inicio=st.integers(1, MINUTOS_NO_DIA - 1),
    termino=st.integers(1, MINUTOS_NO_DIA - 1),
)
def test_termino_depois_da_meia_noite_nunca_vira_o_dia(inicio, termino):
    # Arrange
    cruza = termino <= inicio

    # Act / Assert
    if cruza:
        with pytest.raises(HorarioInvalido):
            IntervaloDeHorario(
                data=HOJE, hora_inicio=hora(inicio), hora_fim=hora(termino)
            )
    else:
        intervalo = IntervaloDeHorario(
            data=HOJE, hora_inicio=hora(inicio), hora_fim=hora(termino)
        )
        assert intervalo.fim().date() == HOJE
