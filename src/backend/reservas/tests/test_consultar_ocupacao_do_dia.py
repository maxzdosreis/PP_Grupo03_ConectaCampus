from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest

from compartilhado.domain.erros import ConflitoDeEstado, RecursoNaoEncontrado
from reservas.application.casos_de_uso import ConsultarOcupacaoDoDia
from reservas.application.ocupacao_do_dia import HorarioOcupado
from reservas.application.portas import EspacoReservavel
from reservas.domain.excecoes import AntecedenciaExcedida, DataRetroativa
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.regras_de_agenda import (
    HORARIO_DE_ABERTURA,
    HORARIO_DE_FECHAMENTO,
    data_limite_para_reservar,
)
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva
from reservas.domain.solicitante import Solicitante
from reservas.tests.fakes import (
    ConsultaDeEspacosEmMemoria,
    RepositorioReservasEmMemoria,
)

S = SituacaoReserva
SAO_PAULO = ZoneInfo("America/Sao_Paulo")
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=SAO_PAULO)
DIA = date(2026, 10, 25)
SOLICITANTE = Solicitante(usuario_id=8, nome="Bruno Lima", matricula="2026002")
QUADRA = EspacoReservavel(id=1, nome="Quadra Coberta")
CAMPO = EspacoReservavel(id=2, nome="Campo Norte")
GINASIO_INATIVO = EspacoReservavel(id=3, nome="Ginásio Antigo")
ID_INEXISTENTE = 9999


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


def _intervalo(inicio, fim, data=DIA):
    return IntervaloDeHorario(
        data=data,
        hora_inicio=time.fromisoformat(inicio),
        hora_fim=time.fromisoformat(fim),
    )


def _salvar(repositorio, situacao, inicio, fim, *, espaco_id=QUADRA.id, data=DIA):
    motivo = "Chuva" if situacao in (S.CANCELADA, S.RECUSADA) else None
    return repositorio.salvar(
        Reserva(
            espaco_id=espaco_id,
            solicitante=SOLICITANTE,
            intervalo=_intervalo(inicio, fim, data),
            finalidade="Treino",
            situacao=situacao,
            motivo_da_situacao=motivo,
            criada_em=AGORA,
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
        HorarioOcupado(intervalo=_intervalo("08:00", "09:00"), situacao=S.SOLICITADA),
        HorarioOcupado(intervalo=_intervalo("10:00", "11:00"), situacao=S.CONFIRMADA),
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
