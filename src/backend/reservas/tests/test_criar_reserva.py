from datetime import date, datetime, time
from zoneinfo import ZoneInfo

import pytest

from compartilhado.domain.erros import ConflitoDeEstado, RecursoNaoEncontrado
from reservas.application.casos_de_uso import CriarReserva
from reservas.application.portas import EspacoReservavel
from reservas.application.repositorio import FiltrosDeReservas
from reservas.domain.excecoes import ConflitoDeHorario, DataRetroativa, HorarioInvalido
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
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
SOLICITANTE = Solicitante(usuario_id=7, nome="Ana Souza", matricula="2026001")
OUTRO_SOLICITANTE = Solicitante(usuario_id=8, nome="Bruno Lima", matricula="2026002")
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
def criar(repositorio, consulta):
    return CriarReserva(repositorio, consulta, lambda: AGORA)


def _dados_validos(**sobrescritas):
    dados = {
        "espaco_id": QUADRA.id,
        "solicitante": SOLICITANTE,
        "data": DIA,
        "hora_inicio": time(10, 0),
        "hora_fim": time(11, 0),
        "finalidade": "Treino de vôlei",
    }
    dados.update(sobrescritas)
    return dados


def _salvar_existente(repositorio, situacao, *, espaco_id=QUADRA.id):
    motivo = "Chuva" if situacao is S.CANCELADA else None
    return repositorio.salvar(
        Reserva(
            espaco_id=espaco_id,
            solicitante=OUTRO_SOLICITANTE,
            intervalo=IntervaloDeHorario(
                data=DIA, hora_inicio=time(10, 0), hora_fim=time(11, 0)
            ),
            finalidade="Jogo marcado",
            situacao=situacao,
            motivo_da_situacao=motivo,
            criada_em=AGORA,
        )
    )


def _todas(repositorio):
    return repositorio.listar(FiltrosDeReservas())


def test_solicitacao_valida_e_salva_como_solicitada(criar, repositorio):
    # Act
    reserva = criar.executar(**_dados_validos())

    # Assert
    assert reserva.id is not None
    assert reserva.situacao is S.SOLICITADA
    assert reserva.criada_em == AGORA
    assert reserva.solicitante == SOLICITANTE
    assert _todas(repositorio) == [reserva]


@pytest.mark.parametrize(
    ("espaco_id", "excecao"),
    [(ID_INEXISTENTE, RecursoNaoEncontrado), (GINASIO_INATIVO.id, ConflitoDeEstado)],
    ids=["espaco-desconhecido", "espaco-inativo"],
)
def test_espaco_indisponivel_propaga_o_erro_sem_salvar(
    criar, repositorio, espaco_id, excecao
):
    # Act
    with pytest.raises(excecao):
        criar.executar(**_dados_validos(espaco_id=espaco_id))

    # Assert
    assert _todas(repositorio) == []


@pytest.mark.parametrize("situacao", [S.SOLICITADA, S.CONFIRMADA])
def test_horario_ocupado_lanca_conflito_sem_salvar(criar, repositorio, situacao):
    # Arrange
    existente = _salvar_existente(repositorio, situacao)

    # Act
    with pytest.raises(ConflitoDeHorario) as erro:
        criar.executar(
            **_dados_validos(hora_inicio=time(10, 30), hora_fim=time(11, 30))
        )

    # Assert
    assert erro.value.situacao is situacao
    assert _todas(repositorio) == [existente]


@pytest.mark.parametrize(
    ("situacao_existente", "espaco_existente", "sobrescritas"),
    [
        (
            S.CONFIRMADA,
            QUADRA.id,
            {"hora_inicio": time(11, 0), "hora_fim": time(12, 0)},
        ),
        (S.CONFIRMADA, CAMPO.id, {}),
        (S.CANCELADA, QUADRA.id, {}),
    ],
    ids=["horario-encostado", "outro-espaco", "ocupado-so-por-cancelada"],
)
def test_horario_livre_salva_a_reserva(
    criar, repositorio, situacao_existente, espaco_existente, sobrescritas
):
    # Arrange
    _salvar_existente(repositorio, situacao_existente, espaco_id=espaco_existente)

    # Act
    reserva = criar.executar(**_dados_validos(**sobrescritas))

    # Assert
    assert reserva.id is not None
    assert len(_todas(repositorio)) == 2


def test_horario_no_passado_lanca_data_retroativa_antes_de_consultar_o_espaco(
    criar, repositorio, consulta
):
    # Act
    with pytest.raises(DataRetroativa):
        criar.executar(**_dados_validos(data=AGORA.date(), hora_inicio=time(9, 0)))

    # Assert
    assert consulta.ids_consultados == []
    assert _todas(repositorio) == []


@pytest.mark.parametrize(
    "hora_fim", [time(10, 0), time(9, 0)], ids=["fim-igual", "fim-antes"]
)
def test_fim_igual_ou_antes_do_inicio_lanca_horario_invalido(
    criar, repositorio, consulta, hora_fim
):
    # Act
    with pytest.raises(HorarioInvalido):
        criar.executar(**_dados_validos(hora_inicio=time(10, 0), hora_fim=hora_fim))

    # Assert
    assert consulta.ids_consultados == []
    assert _todas(repositorio) == []
