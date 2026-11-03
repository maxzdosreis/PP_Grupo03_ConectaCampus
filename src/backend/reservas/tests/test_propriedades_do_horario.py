from datetime import date, timedelta

import pytest
from hypothesis import given
from hypothesis import strategies as st

from reservas.domain.conflito_de_horario import garantir_horario_livre
from reservas.domain.excecoes import ConflitoDeHorario
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.regras_de_agenda import HORARIO_DE_ABERTURA, HORARIO_DE_FECHAMENTO
from reservas.domain.situacao import SITUACOES_QUE_OCUPAM_HORARIO, SituacaoReserva
from reservas.infrastructure.models import ReservaModel
from reservas.infrastructure.repositorio_django import _para_intervalo
from reservas.tests.estrategias import (
    ULTIMO_MINUTO_DO_DIA,
    hora,
    intervalos,
    minutos,
    solicitantes,
)
from reservas.tests.fakes import DIA, UTC, reserva_reconstituida

S = SituacaoReserva
OUTRO_DIA = DIA + timedelta(days=1)
ESPACO = 3
OUTRO_ESPACO = 4
_DUAS_DATAS = st.sampled_from([DIA, OUTRO_DIA])
_OCUPAM = sorted(SITUACOES_QUE_OCUPAM_HORARIO)
_NAO_OCUPAM = sorted(set(SituacaoReserva) - SITUACOES_QUE_OCUPAM_HORARIO)


def _minutos_em_comum(a, b):
    if a.data != b.data:
        return set()
    minutos_de_a = range(minutos(a.hora_inicio), minutos(a.hora_fim))
    return set(minutos_de_a) & set(range(minutos(b.hora_inicio), minutos(b.hora_fim)))


@given(a=intervalos(datas=_DUAS_DATAS), b=intervalos(datas=_DUAS_DATAS))
def test_sobrepoe_e_simetrico(a, b):
    # Act / Assert
    assert a.sobrepoe(b) is b.sobrepoe(a)


@given(a=intervalos(datas=_DUAS_DATAS), b=intervalos(datas=_DUAS_DATAS))
def test_sobrepoe_so_quando_os_intervalos_tem_algum_minuto_em_comum(a, b):
    # Act
    sobrepoe = a.sobrepoe(b)

    # Assert
    assert sobrepoe is bool(_minutos_em_comum(a, b))


@st.composite
def _intervalos_encostados(draw):
    primeiro = draw(intervalos(ate=ULTIMO_MINUTO_DO_DIA - 1))
    fim = draw(st.integers(minutos(primeiro.hora_fim) + 1, ULTIMO_MINUTO_DO_DIA))
    segundo = IntervaloDeHorario(
        data=primeiro.data, hora_inicio=primeiro.hora_fim, hora_fim=hora(fim)
    )
    return draw(st.permutations([primeiro, segundo]))


@given(par=_intervalos_encostados())
def test_intervalos_encostados_nunca_se_sobrepoem(par):
    # Arrange
    a, b = par

    # Act / Assert
    assert not a.sobrepoe(b)


@given(intervalo=intervalos())
def test_todo_intervalo_se_sobrepoe_a_si_mesmo(intervalo):
    # Act / Assert
    assert intervalo.sobrepoe(intervalo)


@st.composite
def _sobreposto_a(draw, alvo):
    inicio = draw(st.integers(0, minutos(alvo.hora_fim) - 1))
    menor_fim = max(inicio, minutos(alvo.hora_inicio)) + 1
    fim = draw(st.integers(menor_fim, ULTIMO_MINUTO_DO_DIA))
    return IntervaloDeHorario(
        data=alvo.data, hora_inicio=hora(inicio), hora_fim=hora(fim)
    )


@st.composite
def _disjunto_de(draw, alvo):
    lados = ["outro_dia"]
    if minutos(alvo.hora_inicio) > 0:
        lados.append("antes")
    if minutos(alvo.hora_fim) < ULTIMO_MINUTO_DO_DIA:
        lados.append("depois")
    lado = draw(st.sampled_from(lados))
    if lado == "antes":
        return draw(intervalos(datas=st.just(alvo.data), ate=minutos(alvo.hora_inicio)))
    if lado == "depois":
        return draw(intervalos(datas=st.just(alvo.data), de=minutos(alvo.hora_fim)))
    return draw(intervalos(datas=st.just(alvo.data + timedelta(days=1))))


@st.composite
def _existente_que_nao_conta(draw, nova):
    motivos = ["outro_espaco", "nao_ocupa", "disjunto"]
    if nova.id is not None:
        motivos.append("a_propria")
    motivo = draw(st.sampled_from(motivos))
    dados = {"espaco_id": ESPACO, "situacao": draw(st.sampled_from(_OCUPAM))}
    dados["intervalo"] = draw(_sobreposto_a(nova.intervalo))
    if motivo == "outro_espaco":
        dados["espaco_id"] = OUTRO_ESPACO
    elif motivo == "nao_ocupa":
        dados["situacao"] = draw(st.sampled_from(_NAO_OCUPAM))
    elif motivo == "disjunto":
        dados["intervalo"] = draw(_disjunto_de(nova.intervalo))
    else:
        dados["id"] = nova.id
    return dados


@st.composite
def _ocupante_de(draw, nova):
    return {
        "espaco_id": ESPACO,
        "situacao": draw(st.sampled_from(_OCUPAM)),
        "intervalo": draw(_sobreposto_a(nova.intervalo)),
    }


@st.composite
def _cenarios_de_conflito(draw, *, min_ocupantes=0):
    nova = reserva_reconstituida(
        id=draw(st.none() | st.just(12)),
        espaco_id=ESPACO,
        intervalo=draw(intervalos()),
    )
    que_nao_contam = draw(st.lists(_existente_que_nao_conta(nova), max_size=5))
    ocupantes = draw(st.lists(_ocupante_de(nova), min_size=min_ocupantes, max_size=3))
    existentes = []
    ids_dos_ocupantes = set()
    for posicao, dados in enumerate(que_nao_contam + ocupantes, start=100):
        dados = {"id": posicao, **dados, "solicitante": draw(solicitantes)}
        existentes.append(reserva_reconstituida(**dados))
        if posicao >= 100 + len(que_nao_contam):
            ids_dos_ocupantes.add(posicao)
    return nova, draw(st.permutations(existentes)), ids_dos_ocupantes


@given(cenario=_cenarios_de_conflito())
def test_so_conta_reserva_do_mesmo_espaco_que_ocupa_horario_e_se_sobrepoe(cenario):
    # Arrange
    nova, existentes, ids_dos_ocupantes = cenario
    ocupantes = [r for r in existentes if r.id in ids_dos_ocupantes]

    # Act / Assert
    if not ocupantes:
        garantir_horario_livre(nova, existentes)
        return
    with pytest.raises(ConflitoDeHorario) as erro:
        garantir_horario_livre(nova, existentes)
    mais_cedo = min(r.intervalo.inicio() for r in ocupantes)
    citados = {
        (r.intervalo, r.situacao)
        for r in ocupantes
        if r.intervalo.inicio() == mais_cedo
    }
    assert (erro.value.intervalo, erro.value.situacao) in citados


def _mensagem_do_conflito(nova, existentes):
    with pytest.raises(ConflitoDeHorario) as erro:
        garantir_horario_livre(nova, existentes)
    return erro.value.mensagem


@given(cenario=_cenarios_de_conflito(min_ocupantes=1), data=st.data())
def test_mensagem_do_conflito_nao_depende_de_quem_reservou(cenario, data):
    # Arrange
    nova, existentes, _ = cenario
    com_outras_pessoas = [
        reserva_reconstituida(
            id=r.id,
            espaco_id=r.espaco_id,
            intervalo=r.intervalo,
            situacao=r.situacao,
            solicitante=data.draw(solicitantes),
        )
        for r in existentes
    ]

    # Act
    mensagem = _mensagem_do_conflito(nova, existentes)

    # Assert
    assert mensagem == _mensagem_do_conflito(nova, com_outras_pessoas)
    assert all(r.solicitante.matricula not in mensagem for r in existentes)


_HORAS_DO_FUNCIONAMENTO = st.lists(
    st.times(min_value=HORARIO_DE_ABERTURA, max_value=HORARIO_DE_FECHAMENTO),
    min_size=2,
    max_size=2,
    unique=True,
).map(sorted)


@given(
    data=st.dates(min_value=date(2000, 1, 1), max_value=date(2100, 12, 31)),
    horas=_HORAS_DO_FUNCIONAMENTO,
)
def test_gravar_em_utc_e_ler_no_fuso_de_sao_paulo_devolve_o_mesmo_intervalo(
    data, horas
):
    # Arrange
    intervalo = IntervaloDeHorario(data=data, hora_inicio=horas[0], hora_fim=horas[1])
    model = ReservaModel(
        inicio=intervalo.inicio().astimezone(UTC), fim=intervalo.fim().astimezone(UTC)
    )

    # Act
    lido = _para_intervalo(model)

    # Assert
    assert lido == intervalo
