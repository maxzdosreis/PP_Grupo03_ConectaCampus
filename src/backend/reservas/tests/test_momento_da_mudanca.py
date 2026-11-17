from datetime import datetime, time, timedelta
from itertools import product

import pytest

from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.excecoes import (
    AlteracaoDeSituacaoNaoPermitida,
    ConclusaoAntesDoTermino,
    MotivoObrigatorio,
    MudancaAposOInicio,
    TransicaoDeSituacaoInvalida,
)
from reservas.domain.intervalo_de_horario import FUSO_HORARIO
from reservas.domain.situacao import SituacaoReserva as S
from reservas.domain.situacao import momento_permite
from reservas.tests.fakes import (
    ANA,
    DIA,
    GESTOR,
    MOTIVO,
    UTC,
    exatamente,
    intervalo,
    reserva_reconstituida,
)

P = PapelDoAtor
MICROSSEGUNDO = timedelta(microseconds=1)
INICIO = intervalo().inicio()
TERMINO = intervalo().fim()
ATOR_DONO = Ator(usuario_id=ANA.usuario_id, nome=ANA.nome, papel=P.SOLICITANTE)

MOMENTOS = {
    "bem_antes_do_inicio": INICIO - timedelta(days=3),
    "1us_antes_do_inicio": INICIO - MICROSSEGUNDO,
    "exatamente_no_inicio": INICIO,
    "durante": INICIO + timedelta(minutes=30),
    "1us_antes_do_termino": TERMINO - MICROSSEGUNDO,
    "exatamente_no_termino": TERMINO,
    "depois_do_termino": TERMINO + timedelta(hours=5),
}
ANTES_DO_INICIO = {"bem_antes_do_inicio", "1us_antes_do_inicio"}
A_PARTIR_DO_TERMINO = {"exatamente_no_termino", "depois_do_termino"}


def _ator(papel):
    return GESTOR if papel is P.GESTOR else ATOR_DONO


def _aceito_pela_regra_do_momento(papel, nova, momento):
    if papel is P.SOLICITANTE:
        return True
    if nova is S.CONCLUIDA:
        return momento in A_PARTIR_DO_TERMINO
    if nova in {S.RECUSADA, S.CANCELADA}:
        return momento in ANTES_DO_INICIO
    return True


def _alterar(reserva, nova, papel, agora):
    reserva.alterar_situacao(nova, motivo=MOTIVO, ator=_ator(papel), agora=agora)


TRANSICOES_DO_GESTOR = [
    (S.SOLICITADA, S.CONFIRMADA),
    (S.SOLICITADA, S.RECUSADA),
    (S.SOLICITADA, S.CANCELADA),
    (S.CONFIRMADA, S.CONCLUIDA),
    (S.CONFIRMADA, S.CANCELADA),
]
CASOS = [
    (P.GESTOR, atual, nova, momento)
    for (atual, nova), momento in product(TRANSICOES_DO_GESTOR, MOMENTOS)
] + [
    (P.SOLICITANTE, atual, S.CANCELADA, momento)
    for atual, momento in product((S.SOLICITADA, S.CONFIRMADA), MOMENTOS)
]
IDS = [f"{p.name}-{a.name}->{n.name}-{m}" for p, a, n, m in CASOS]


@pytest.mark.parametrize(
    ("papel", "atual", "nova", "momento"),
    CASOS,
    ids=IDS,
)
def test_alteracao_segue_a_regra_do_momento_da_dec_13(papel, atual, nova, momento):
    # Arrange
    reserva = reserva_reconstituida(situacao=atual)
    agora = MOMENTOS[momento]
    aceito = _aceito_pela_regra_do_momento(papel, nova, momento)

    # Act / Assert
    if aceito:
        _alterar(reserva, nova, papel, agora)
        assert reserva.situacao is nova
        return
    excecao = ConclusaoAntesDoTermino if nova is S.CONCLUIDA else MudancaAposOInicio
    with pytest.raises(excecao):
        _alterar(reserva, nova, papel, agora)
    assert reserva.situacao is atual
    assert reserva.registros_pendentes == ()


@pytest.mark.parametrize(
    ("papel", "atual", "nova", "momento"),
    CASOS,
    ids=IDS,
)
def test_acoes_oferecidas_coincidem_com_o_que_a_alteracao_aceita(
    papel, atual, nova, momento
):
    # Arrange
    reserva = reserva_reconstituida(situacao=atual)
    agora = MOMENTOS[momento]

    # Act
    oferecida = nova in reserva.acoes_permitidas_para(_ator(papel), agora)

    # Assert
    assert oferecida is _aceito_pela_regra_do_momento(papel, nova, momento)


def tabela_do_gestor() -> list[str]:
    linhas = []
    for atual, nova in TRANSICOES_DO_GESTOR:
        reserva = reserva_reconstituida(situacao=atual)
        celulas = [
            "SIM" if nova in reserva.acoes_permitidas_para(GESTOR, agora) else "nao"
            for agora in MOMENTOS.values()
        ]
        linhas.append(f"{atual.name} -> {nova.name}: " + " ".join(celulas))
    return linhas


def test_tabela_situacao_acao_momento_do_gestor():
    # Act
    linhas = tabela_do_gestor()

    # Assert
    assert linhas == [
        "SOLICITADA -> CONFIRMADA: SIM SIM SIM SIM SIM SIM SIM",
        "SOLICITADA -> RECUSADA: SIM SIM nao nao nao nao nao",
        "SOLICITADA -> CANCELADA: SIM SIM nao nao nao nao nao",
        "CONFIRMADA -> CONCLUIDA: nao nao nao nao nao SIM SIM",
        "CONFIRMADA -> CANCELADA: SIM SIM nao nao nao nao nao",
    ]


@pytest.mark.parametrize("momento", MOMENTOS)
def test_solicitada_vencida_continua_aceitando_confirmar_e_o_cancelamento_do_dono(
    momento,
):
    # Arrange
    agora = MOMENTOS[momento]

    # Act / Assert
    confirmada = reserva_reconstituida(situacao=S.SOLICITADA)
    _alterar(confirmada, S.CONFIRMADA, P.GESTOR, agora)
    cancelada = reserva_reconstituida(situacao=S.SOLICITADA)
    _alterar(cancelada, S.CANCELADA, P.SOLICITANTE, agora)
    assert (confirmada.situacao, cancelada.situacao) == (S.CONFIRMADA, S.CANCELADA)


def test_mensagem_de_concluir_antes_do_termino_informa_data_e_hora_do_termino():
    # Arrange
    reserva = reserva_reconstituida(situacao=S.CONFIRMADA)

    # Act / Assert
    with pytest.raises(
        ConclusaoAntesDoTermino,
        match=exatamente(
            "Só é possível concluir a reserva a partir do término dela "
            "(25/10/2026 às 11:00)."
        ),
    ) as erro:
        _alterar(reserva, S.CONCLUIDA, P.GESTOR, INICIO)
    assert erro.value.codigo == "CONCLUSAO_ANTES_DO_TERMINO"
    assert erro.value.termino == TERMINO


@pytest.mark.parametrize(
    ("nova", "verbo"), [(S.RECUSADA, "recusar"), (S.CANCELADA, "cancelar")]
)
def test_mensagem_de_recusar_ou_cancelar_apos_o_inicio_diz_o_verbo_e_o_inicio(
    nova, verbo
):
    # Arrange
    reserva = reserva_reconstituida(situacao=S.SOLICITADA)

    # Act / Assert
    with pytest.raises(
        MudancaAposOInicio,
        match=exatamente(
            f"Só é possível {verbo} a reserva antes do início dela "
            "(25/10/2026 às 10:00)."
        ),
    ) as erro:
        _alterar(reserva, nova, P.GESTOR, INICIO)
    assert erro.value.codigo == "RECUSA_OU_CANCELAMENTO_APOS_O_INICIO"
    assert erro.value.nova is nova


def test_momento_vem_depois_da_transicao_e_antes_do_motivo():
    # Arrange
    gestor = GESTOR

    # Act / Assert
    concluida = reserva_reconstituida(situacao=S.SOLICITADA)
    with pytest.raises(TransicaoDeSituacaoInvalida):
        concluida.alterar_situacao(
            S.CONCLUIDA, ator=gestor, agora=INICIO - timedelta(days=1)
        )
    # momento vence o motivo ausente
    solicitada = reserva_reconstituida(situacao=S.SOLICITADA)
    with pytest.raises(MudancaAposOInicio):
        solicitada.alterar_situacao(S.RECUSADA, ator=gestor, agora=INICIO)
    # sem erro de momento, o motivo ausente é recusado
    with pytest.raises(MotivoObrigatorio):
        solicitada.alterar_situacao(
            S.RECUSADA, ator=gestor, agora=INICIO - MICROSSEGUNDO
        )


def test_permissao_vem_antes_do_momento():
    # Arrange
    reserva = reserva_reconstituida(situacao=S.CONFIRMADA)

    # Act / Assert: Solicitante concluindo antes do término recebe 403, não 409
    with pytest.raises(AlteracaoDeSituacaoNaoPermitida):
        reserva.alterar_situacao(
            S.CONCLUIDA, ator=ATOR_DONO, agora=INICIO - timedelta(days=1)
        )


def test_comparacao_usa_instantes_e_nao_o_fuso_de_quem_pergunta():
    # Arrange
    reserva = reserva_reconstituida(
        situacao=S.CONFIRMADA, intervalo=intervalo("23:30", "23:59")
    )
    fim_em_utc = reserva.intervalo.fim().astimezone(UTC)

    # Act
    antes = reserva.acoes_permitidas_para(
        GESTOR, reserva.intervalo.fim() - MICROSSEGUNDO
    )
    no_fim = reserva.acoes_permitidas_para(GESTOR, fim_em_utc)

    # Assert
    assert S.CONCLUIDA not in antes
    assert S.CONCLUIDA in no_fim


def test_virada_de_dia_reserva_de_ontem_pode_ser_concluida_hoje_cedo():
    # Arrange
    reserva = reserva_reconstituida(
        situacao=S.CONFIRMADA, intervalo=intervalo("22:00", "23:59")
    )
    meia_noite = datetime.combine(DIA + timedelta(days=1), time(0, 0), FUSO_HORARIO)

    # Act
    acoes = reserva.acoes_permitidas_para(GESTOR, meia_noite)

    # Assert
    assert S.CONCLUIDA in acoes
    assert S.CANCELADA not in acoes


def test_reserva_nao_visivel_nao_tem_acoes_em_nenhum_momento():
    # Arrange
    outra = Ator(usuario_id=99, nome="Outra", papel=P.SOLICITANTE)

    # Act / Assert
    assert reserva_reconstituida().acoes_permitidas_para(outra, TERMINO) == []


def test_acoes_permitidas_exige_agora_com_fuso():
    # Act / Assert
    with pytest.raises(TypeError):
        reserva_reconstituida().acoes_permitidas_para(GESTOR, datetime(2026, 10, 25))


@pytest.mark.parametrize(
    ("papel", "nova", "agora", "esperado"),
    [
        (P.GESTOR, S.CONCLUIDA, TERMINO, True),
        (P.GESTOR, S.CONCLUIDA, TERMINO - MICROSSEGUNDO, False),
        (P.GESTOR, S.RECUSADA, INICIO - MICROSSEGUNDO, True),
        (P.GESTOR, S.CANCELADA, INICIO, False),
        (P.GESTOR, S.CONFIRMADA, TERMINO + timedelta(days=9), True),
        (P.SOLICITANTE, S.CANCELADA, TERMINO + timedelta(days=9), True),
    ],
)
def test_momento_permite_e_a_regra_pura_da_dec_13(papel, nova, agora, esperado):
    # Act
    resultado = momento_permite(papel, nova, inicio=INICIO, fim=TERMINO, agora=agora)

    # Assert
    assert resultado is esperado
