from datetime import date, datetime, time
from zoneinfo import ZoneInfo

import pytest

from reservas.application.casos_de_uso import ConsultarReservas, ObterReserva
from reservas.application.repositorio import FiltrosDeReservas
from reservas.domain.excecoes import ReservaNaoEncontrada
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva
from reservas.domain.solicitante import Solicitante
from reservas.tests.fakes import RepositorioReservasEmMemoria

SAO_PAULO = ZoneInfo("America/Sao_Paulo")
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=SAO_PAULO)
DIA = date(2026, 10, 25)
ANA = Solicitante(usuario_id=7, nome="Ana Souza", matricula="2026001")
BRUNO = Solicitante(usuario_id=8, nome="Bruno Lima", matricula="2026002")
QUADRA = 1
CAMPO = 2
ID_INEXISTENTE = 9999


@pytest.fixture
def repositorio():
    return RepositorioReservasEmMemoria()


@pytest.fixture
def ids(repositorio):
    """Salva fora da ordem de início para provar a ordenação."""
    tarde = _salvar(repositorio, QUADRA, ANA, time(14, 0), time(15, 0))
    manha = _salvar(repositorio, CAMPO, BRUNO, time(9, 0), time(10, 0))
    meio_dia = _salvar(repositorio, QUADRA, BRUNO, time(11, 0), time(12, 0))
    return {"tarde": tarde.id, "manha": manha.id, "meio_dia": meio_dia.id}


def _salvar(repositorio, espaco_id, solicitante, hora_inicio, hora_fim):
    reserva = Reserva.solicitar(
        espaco_id=espaco_id,
        solicitante=solicitante,
        data=DIA,
        hora_inicio=hora_inicio,
        hora_fim=hora_fim,
        finalidade="Treino",
        agora=AGORA,
    )
    return repositorio.salvar(reserva)


def _ids_de(reservas):
    return [reserva.id for reserva in reservas]


def test_consultar_sem_filtros_devolve_todas_por_inicio(repositorio, ids):
    # Act
    reservas = ConsultarReservas(repositorio).executar(FiltrosDeReservas())

    # Assert
    assert _ids_de(reservas) == [ids["manha"], ids["meio_dia"], ids["tarde"]]


@pytest.mark.parametrize(
    "filtros",
    [
        FiltrosDeReservas(espaco_id=QUADRA),
        FiltrosDeReservas(solicitante="bruno"),
        FiltrosDeReservas(espaco_id=QUADRA, solicitante_usuario_id=BRUNO.usuario_id),
        FiltrosDeReservas(situacao=SituacaoReserva.CONFIRMADA),
    ],
    ids=["espaco", "solicitante", "espaco-e-usuario", "sem-resultado"],
)
def test_consultar_repassa_os_filtros_ao_repositorio(repositorio, ids, filtros):
    # Act
    reservas = ConsultarReservas(repositorio).executar(filtros)

    # Assert
    assert _ids_de(reservas) == _ids_de(repositorio.listar(filtros))


def test_consultar_combina_os_filtros(repositorio, ids):
    # Act
    reservas = ConsultarReservas(repositorio).executar(
        FiltrosDeReservas(espaco_id=QUADRA, solicitante="bruno")
    )

    # Assert
    assert _ids_de(reservas) == [ids["meio_dia"]]


def test_obter_devolve_a_reserva(repositorio, ids):
    # Act
    reserva = ObterReserva(repositorio).executar(ids["tarde"])

    # Assert
    assert reserva.id == ids["tarde"]
    assert reserva.solicitante == ANA
    assert reserva.espaco_id == QUADRA


def test_obter_id_inexistente_lanca_reserva_nao_encontrada(repositorio):
    # Act / Assert
    with pytest.raises(ReservaNaoEncontrada) as erro:
        ObterReserva(repositorio).executar(ID_INEXISTENTE)

    assert erro.value.reserva_id == ID_INEXISTENTE
    assert erro.value.mensagem == f"Reserva de código {ID_INEXISTENTE} não encontrada."
