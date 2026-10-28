from datetime import date, datetime, time
from zoneinfo import ZoneInfo

import pytest

from reservas.application.casos_de_uso import AlterarSituacaoReserva
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.excecoes import (
    AlteracaoDeSituacaoNaoPermitida,
    MotivoObrigatorio,
    ReservaNaoEncontrada,
    SituacaoInvalida,
    TransicaoDeSituacaoInvalida,
)
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import (
    SITUACOES_QUE_EXIGEM_MOTIVO,
    TRANSICOES_PERMITIDAS,
    SituacaoReserva,
)
from reservas.domain.solicitante import Solicitante
from reservas.tests.fakes import RepositorioReservasEmMemoria

SAO_PAULO = ZoneInfo("America/Sao_Paulo")
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=SAO_PAULO)
ANA = Solicitante(usuario_id=7, nome="Ana Souza", matricula="2026001")
GESTOR = Ator(usuario_id=1, nome="Gestora de Teste", papel=PapelDoAtor.GESTOR)
INTERVALO = IntervaloDeHorario(
    data=date(2026, 10, 25), hora_inicio=time(10, 0), hora_fim=time(11, 0)
)
MOTIVO = "Chuva forte"
ID_INEXISTENTE = 9999

TRANSICOES_VALIDAS = [
    (atual, nova)
    for atual, destinos in TRANSICOES_PERMITIDAS.items()
    for nova in sorted(destinos)
]
TRANSICOES_PROIBIDAS = [
    (atual, nova)
    for atual in SituacaoReserva
    for nova in SituacaoReserva
    if nova not in TRANSICOES_PERMITIDAS[atual]
]
TRANSICOES_QUE_EXIGEM_MOTIVO = [
    (atual, nova)
    for atual, nova in TRANSICOES_VALIDAS
    if nova in SITUACOES_QUE_EXIGEM_MOTIVO
]


def relogio_fixo():
    return AGORA


def _nomes(transicoes):
    return [f"{atual}->{nova}" for atual, nova in transicoes]


@pytest.fixture
def repositorio():
    return RepositorioReservasEmMemoria()


def _salvar_em(repositorio, situacao):
    reserva = Reserva(
        espaco_id=1,
        solicitante=ANA,
        intervalo=INTERVALO,
        finalidade="Treino",
        situacao=situacao,
        motivo_da_situacao=_motivo_para(situacao),
        criada_em=AGORA,
    )
    return repositorio.salvar(reserva)


def _motivo_para(situacao):
    return MOTIVO if situacao in SITUACOES_QUE_EXIGEM_MOTIVO else None


def _retrato(repositorio, reserva_id):
    reserva = repositorio.obter_por_id(reserva_id)
    return reserva.situacao, reserva.motivo_da_situacao


@pytest.mark.parametrize(
    ("atual", "nova"), TRANSICOES_VALIDAS, ids=_nomes(TRANSICOES_VALIDAS)
)
def test_transicao_permitida_e_persistida(repositorio, atual, nova):
    # Arrange
    reserva = _salvar_em(repositorio, atual)

    # Act
    alterada = AlterarSituacaoReserva(repositorio, relogio_fixo).executar(
        ator=GESTOR,
        reserva_id=reserva.id,
        nova_situacao=nova,
        motivo=_motivo_para(nova),
    )

    # Assert
    assert alterada.situacao == nova
    assert repositorio.obter_por_id(reserva.id).situacao == nova


@pytest.mark.parametrize(
    ("atual", "nova"), TRANSICOES_PROIBIDAS, ids=_nomes(TRANSICOES_PROIBIDAS)
)
def test_transicao_proibida_lanca_erro_e_preserva_a_reserva(repositorio, atual, nova):
    # Arrange
    reserva = _salvar_em(repositorio, atual)
    antes = _retrato(repositorio, reserva.id)

    # Act / Assert
    with pytest.raises(TransicaoDeSituacaoInvalida) as erro:
        AlterarSituacaoReserva(repositorio, relogio_fixo).executar(
            ator=GESTOR,
            reserva_id=reserva.id,
            nova_situacao=nova,
            motivo="Qualquer motivo",
        )

    assert (erro.value.atual, erro.value.nova) == (atual, nova)
    assert _retrato(repositorio, reserva.id) == antes


@pytest.mark.parametrize("motivo", [None, "", "   "], ids=["none", "vazio", "espacos"])
@pytest.mark.parametrize(
    ("atual", "nova"),
    TRANSICOES_QUE_EXIGEM_MOTIVO,
    ids=_nomes(TRANSICOES_QUE_EXIGEM_MOTIVO),
)
def test_recusar_ou_cancelar_sem_motivo_lanca_erro_e_preserva_a_reserva(
    repositorio, atual, nova, motivo
):
    # Arrange
    reserva = _salvar_em(repositorio, atual)
    antes = _retrato(repositorio, reserva.id)

    # Act / Assert
    with pytest.raises(MotivoObrigatorio):
        AlterarSituacaoReserva(repositorio, relogio_fixo).executar(
            ator=GESTOR, reserva_id=reserva.id, nova_situacao=nova, motivo=motivo
        )

    assert _retrato(repositorio, reserva.id) == antes


def test_cancelar_guarda_o_motivo_normalizado(repositorio):
    # Arrange
    reserva = _salvar_em(repositorio, SituacaoReserva.SOLICITADA)

    # Act
    AlterarSituacaoReserva(repositorio, relogio_fixo).executar(
        ator=GESTOR,
        reserva_id=reserva.id,
        nova_situacao=SituacaoReserva.CANCELADA,
        motivo="  Chuva   forte ",
    )

    # Assert
    assert _retrato(repositorio, reserva.id) == (SituacaoReserva.CANCELADA, MOTIVO)


def test_confirmar_sem_motivo_deixa_o_motivo_vazio(repositorio):
    # Arrange
    reserva = _salvar_em(repositorio, SituacaoReserva.SOLICITADA)

    # Act
    AlterarSituacaoReserva(repositorio, relogio_fixo).executar(
        ator=GESTOR, reserva_id=reserva.id, nova_situacao=SituacaoReserva.CONFIRMADA
    )

    # Assert
    assert _retrato(repositorio, reserva.id) == (SituacaoReserva.CONFIRMADA, None)


def test_situacao_como_texto_e_aceita(repositorio):
    # Arrange
    reserva = _salvar_em(repositorio, SituacaoReserva.SOLICITADA)

    # Act
    alterada = AlterarSituacaoReserva(repositorio, relogio_fixo).executar(
        ator=GESTOR, reserva_id=reserva.id, nova_situacao="CONFIRMADA"
    )

    # Assert
    assert alterada.situacao is SituacaoReserva.CONFIRMADA


def test_situacao_desconhecida_lanca_erro_e_preserva_a_reserva(repositorio):
    # Arrange
    reserva = _salvar_em(repositorio, SituacaoReserva.SOLICITADA)

    # Act / Assert
    with pytest.raises(SituacaoInvalida):
        AlterarSituacaoReserva(repositorio, relogio_fixo).executar(
            ator=GESTOR, reserva_id=reserva.id, nova_situacao="PENDENTE"
        )

    assert _retrato(repositorio, reserva.id) == (SituacaoReserva.SOLICITADA, None)


def test_reserva_inexistente_lanca_reserva_nao_encontrada(repositorio):
    # Act / Assert
    with pytest.raises(ReservaNaoEncontrada) as erro:
        AlterarSituacaoReserva(repositorio, relogio_fixo).executar(
            ator=GESTOR,
            reserva_id=ID_INEXISTENTE,
            nova_situacao=SituacaoReserva.CONFIRMADA,
        )

    assert erro.value.reserva_id == ID_INEXISTENTE


def test_ciclo_solicitada_confirmada_concluida(repositorio):
    # Arrange
    reserva = _salvar_em(repositorio, SituacaoReserva.SOLICITADA)
    alterar = AlterarSituacaoReserva(repositorio, relogio_fixo)

    # Act
    alterar.executar(
        ator=GESTOR, reserva_id=reserva.id, nova_situacao=SituacaoReserva.CONFIRMADA
    )
    alterar.executar(
        ator=GESTOR, reserva_id=reserva.id, nova_situacao=SituacaoReserva.CONCLUIDA
    )

    # Assert
    concluida = repositorio.obter_por_id(reserva.id)
    assert concluida.situacao is SituacaoReserva.CONCLUIDA
    assert concluida.situacao.eh_final


def test_solicitante_cancela_a_propria_reserva(repositorio):
    # Arrange
    reserva = _salvar_em(repositorio, SituacaoReserva.SOLICITADA)
    dona = Ator(usuario_id=ANA.usuario_id, nome=ANA.nome, papel=PapelDoAtor.SOLICITANTE)

    # Act
    AlterarSituacaoReserva(repositorio, relogio_fixo).executar(
        reserva_id=reserva.id,
        nova_situacao=SituacaoReserva.CANCELADA,
        motivo=MOTIVO,
        ator=dona,
    )

    # Assert
    assert _retrato(repositorio, reserva.id) == (SituacaoReserva.CANCELADA, MOTIVO)


def test_solicitante_confirmando_a_propria_lanca_nao_permitida_e_preserva(
    repositorio,
):
    # Arrange
    reserva = _salvar_em(repositorio, SituacaoReserva.SOLICITADA)
    dona = Ator(usuario_id=ANA.usuario_id, nome=ANA.nome, papel=PapelDoAtor.SOLICITANTE)

    # Act / Assert
    with pytest.raises(AlteracaoDeSituacaoNaoPermitida):
        AlterarSituacaoReserva(repositorio, relogio_fixo).executar(
            reserva_id=reserva.id,
            nova_situacao=SituacaoReserva.CONFIRMADA,
            ator=dona,
        )

    assert _retrato(repositorio, reserva.id) == (SituacaoReserva.SOLICITADA, None)


def test_reserva_de_outra_pessoa_para_o_solicitante_lanca_nao_encontrada(
    repositorio,
):
    # Arrange
    reserva = _salvar_em(repositorio, SituacaoReserva.SOLICITADA)
    outra_pessoa = Ator(
        usuario_id=99, nome="Solicitante de Teste", papel=PapelDoAtor.SOLICITANTE
    )

    # Act / Assert
    with pytest.raises(ReservaNaoEncontrada) as erro:
        AlterarSituacaoReserva(repositorio, relogio_fixo).executar(
            reserva_id=reserva.id,
            nova_situacao=SituacaoReserva.CANCELADA,
            motivo=MOTIVO,
            ator=outra_pessoa,
        )

    assert erro.value.reserva_id == reserva.id
    assert _retrato(repositorio, reserva.id) == (SituacaoReserva.SOLICITADA, None)


def test_registro_da_mudanca_usa_o_relogio_injetado_e_o_ator(repositorio):
    # Arrange
    reserva = _salvar_em(repositorio, SituacaoReserva.SOLICITADA)

    # Act
    AlterarSituacaoReserva(repositorio, relogio_fixo).executar(
        ator=GESTOR,
        reserva_id=reserva.id,
        nova_situacao=SituacaoReserva.CANCELADA,
        motivo=MOTIVO,
    )

    # Assert
    (registro,) = repositorio.listar_historico(reserva.id)
    assert registro.registrado_em == AGORA
    assert (registro.autor_usuario_id, registro.autor_nome) == (1, GESTOR.nome)
    assert (registro.situacao_anterior, registro.situacao_nova, registro.motivo) == (
        SituacaoReserva.SOLICITADA,
        SituacaoReserva.CANCELADA,
        MOTIVO,
    )


def test_alteracao_recusada_nao_registra_no_historico(repositorio):
    # Arrange
    reserva = _salvar_em(repositorio, SituacaoReserva.SOLICITADA)

    # Act
    with pytest.raises(MotivoObrigatorio):
        AlterarSituacaoReserva(repositorio, relogio_fixo).executar(
            ator=GESTOR, reserva_id=reserva.id, nova_situacao=SituacaoReserva.RECUSADA
        )

    # Assert
    assert repositorio.listar_historico(reserva.id) == []
