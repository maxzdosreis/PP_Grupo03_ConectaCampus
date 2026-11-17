from datetime import datetime, time, timedelta

import pytest

from compartilhado.domain.erros import ConflitoDeEstado, RecursoNaoEncontrado
from reservas.application.casos_de_uso import ConsultarOcupacaoDoDia
from reservas.application.ocupacao_do_dia import HorarioOcupado
from reservas.domain.excecoes import AntecedenciaExcedida, DataRetroativa
from reservas.domain.intervalo_de_horario import FUSO_HORARIO
from reservas.domain.regras_de_agenda import data_limite_para_reservar
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import (
    AGORA,
    BRUNO,
    DIA,
    ID_INEXISTENTE,
    ConsultaDeEspacosEmMemoria,
    RepositorioReservasEmMemoria,
    espaco_reservavel,
    funcionamento,
    intervalo,
    reserva_reconstituida,
)

S = SituacaoReserva
QUADRA = espaco_reservavel(1, "Quadra Coberta")
CAMPO = espaco_reservavel(2, "Campo Norte")
GINASIO_INATIVO = espaco_reservavel(3, "Ginásio Antigo")
QUADRA_DE_DIA = espaco_reservavel(4, "Quadra de Dia", funcionamento("08:00", "18:00"))


@pytest.fixture
def repositorio():
    return RepositorioReservasEmMemoria()


@pytest.fixture
def consulta():
    return ConsultaDeEspacosEmMemoria(
        [QUADRA, CAMPO, GINASIO_INATIVO, QUADRA_DE_DIA],
        ids_inativos=[GINASIO_INATIVO.id],
    )


@pytest.fixture
def consultar(repositorio, consulta):
    return ConsultarOcupacaoDoDia(repositorio, consulta, lambda: AGORA)


def _salvar(repositorio, situacao, inicio, fim, *, espaco_id=QUADRA.id, data=DIA):
    return repositorio.salvar(
        reserva_reconstituida(
            id=None,
            espaco_id=espaco_id,
            solicitante=BRUNO,
            intervalo=intervalo(inicio, fim, data),
            situacao=situacao,
        )
    )


def _livres_como_texto(ocupacao):
    return [
        f"{livre.hora_inicio:%H:%M}–{livre.hora_fim:%H:%M}" for livre in ocupacao.livres
    ]


def test_espaco_desconhecido_e_recurso_nao_encontrado(consultar):
    # Act / Assert
    with pytest.raises(RecursoNaoEncontrado):
        consultar.executar(espaco_id=ID_INEXISTENTE, data=DIA)


def test_espaco_inativo_e_conflito_de_estado(consultar, consulta):
    # Act / Assert
    with pytest.raises(ConflitoDeEstado):
        consultar.executar(espaco_id=GINASIO_INATIVO.id, data=DIA)
    assert consulta.ids_consultados == [GINASIO_INATIVO.id]


def test_dia_sem_reservas_tem_o_funcionamento_inteiro_livre(consultar):
    # Act
    ocupacao = consultar.executar(espaco_id=QUADRA.id, data=DIA)

    # Assert
    assert ocupacao.data == DIA
    assert ocupacao.horario_de_abertura == time(7, 0)
    assert ocupacao.horario_de_fechamento == time(0, 0)
    assert ocupacao.ocupados == ()
    assert _livres_como_texto(ocupacao) == ["07:00–00:00"]
    assert ocupacao.reservavel is True
    assert ocupacao.motivo_indisponivel is None


def test_so_solicitadas_e_confirmadas_ocupam_e_o_resto_fica_livre(
    consultar, repositorio
):
    # Arrange
    _salvar(repositorio, S.CONFIRMADA, "10:00", "11:00")
    _salvar(repositorio, S.SOLICITADA, "08:00", "09:00")
    _salvar(repositorio, S.CANCELADA, "14:00", "15:00")
    _salvar(repositorio, S.RECUSADA, "16:00", "17:00")
    _salvar(repositorio, S.CONFIRMADA, "18:00", "19:00", espaco_id=CAMPO.id)
    _salvar(repositorio, S.CONFIRMADA, "12:00", "13:00", data=DIA + timedelta(days=1))

    # Act
    ocupacao = consultar.executar(espaco_id=QUADRA.id, data=DIA)

    # Assert
    assert ocupacao.ocupados == (
        HorarioOcupado(intervalo=intervalo("08:00", "09:00"), situacao=S.SOLICITADA),
        HorarioOcupado(intervalo=intervalo("10:00", "11:00"), situacao=S.CONFIRMADA),
    )
    assert _livres_como_texto(ocupacao) == [
        "07:00–08:00",
        "09:00–10:00",
        "11:00–00:00",
    ]


@pytest.mark.parametrize(
    ("data", "mensagem"),
    [
        (AGORA.date() - timedelta(days=1), DataRetroativa().mensagem),
        (
            AGORA.date() + timedelta(days=31),
            AntecedenciaExcedida(30, data_limite_para_reservar(AGORA)).mensagem,
        ),
    ],
    ids=["ontem", "alem-da-antecedencia"],
)
def test_data_indisponivel_nao_tem_livres_e_traz_o_motivo(
    consultar, repositorio, data, mensagem
):
    # Arrange
    _salvar(repositorio, S.CONFIRMADA, "10:00", "11:00", data=data)

    # Act
    ocupacao = consultar.executar(espaco_id=QUADRA.id, data=data)

    # Assert
    assert ocupacao.reservavel is False
    assert ocupacao.motivo_indisponivel == mensagem
    assert ocupacao.livres == ()
    assert len(ocupacao.ocupados) == 1


def test_espaco_com_horario_proprio_mostra_a_sua_janela_e_os_livres_dela(
    consultar, repositorio
):
    # Arrange
    _salvar(repositorio, S.CONFIRMADA, "12:00", "13:00", espaco_id=QUADRA_DE_DIA.id)

    # Act
    ocupacao = consultar.executar(espaco_id=QUADRA_DE_DIA.id, data=DIA)

    # Assert
    assert ocupacao.horario_de_abertura == time(8, 0)
    assert ocupacao.horario_de_fechamento == time(18, 0)
    assert _livres_como_texto(ocupacao) == ["08:00–12:00", "13:00–18:00"]


def test_reserva_ate_a_meia_noite_aparece_na_agenda_do_dia_dela_e_nao_na_do_seguinte(
    consultar, repositorio
):
    # Arrange
    _salvar(repositorio, S.SOLICITADA, "23:00", "00:00")

    # Act
    do_dia = consultar.executar(espaco_id=QUADRA.id, data=DIA)
    do_seguinte = consultar.executar(espaco_id=QUADRA.id, data=DIA + timedelta(days=1))

    # Assert
    assert [h.intervalo for h in do_dia.ocupados] == [intervalo("23:00", "00:00")]
    assert _livres_como_texto(do_dia) == ["07:00–23:00"]
    assert do_seguinte.ocupados == ()
    assert _livres_como_texto(do_seguinte) == ["07:00–00:00"]


def test_hoje_depois_do_fechamento_do_espaco_nao_e_reservavel(repositorio, consulta):
    # Arrange
    agora = datetime(2026, 10, 21, 18, 30, tzinfo=FUSO_HORARIO)
    consultar = ConsultarOcupacaoDoDia(repositorio, consulta, lambda: agora)

    # Act
    de_dia = consultar.executar(espaco_id=QUADRA_DE_DIA.id, data=agora.date())
    padrao = consultar.executar(espaco_id=QUADRA.id, data=agora.date())

    # Assert
    assert de_dia.reservavel is False
    assert de_dia.motivo_indisponivel == DataRetroativa().mensagem
    assert padrao.reservavel is True
