from datetime import timedelta

import pytest

from compartilhado.domain.erros import ConflitoDeEstado, RecursoNaoEncontrado
from reservas.application.casos_de_uso import ConsultarOcupacaoDoDia
from reservas.application.ocupacao_do_dia import HorarioOcupado
from reservas.application.portas import EspacoReservavel
from reservas.domain.excecoes import AntecedenciaExcedida, DataRetroativa
from reservas.domain.regras_de_agenda import (
    HORARIO_DE_ABERTURA,
    HORARIO_DE_FECHAMENTO,
    data_limite_para_reservar,
)
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import (
    AGORA,
    BRUNO,
    DIA,
    ID_INEXISTENTE,
    ConsultaDeEspacosEmMemoria,
    RepositorioReservasEmMemoria,
    intervalo,
    reserva_reconstituida,
)

S = SituacaoReserva
QUADRA = EspacoReservavel(id=1, nome="Quadra Coberta")
CAMPO = EspacoReservavel(id=2, nome="Campo Norte")
GINASIO_INATIVO = EspacoReservavel(id=3, nome="Ginásio Antigo")


@pytest.fixture
def repositorio():
    return RepositorioReservasEmMemoria()


@pytest.fixture
def consulta():
    return ConsultaDeEspacosEmMemoria(
        [QUADRA, CAMPO, GINASIO_INATIVO], ids_inativos=[GINASIO_INATIVO.id]
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
    assert ocupacao.horario_de_abertura == HORARIO_DE_ABERTURA
    assert ocupacao.horario_de_fechamento == HORARIO_DE_FECHAMENTO
    assert ocupacao.ocupados == ()
    assert _livres_como_texto(ocupacao) == ["07:00–22:00"]
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
        "11:00–22:00",
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
