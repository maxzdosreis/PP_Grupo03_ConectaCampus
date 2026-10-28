from datetime import date, datetime, time
from zoneinfo import ZoneInfo

import pytest

from reservas.application.casos_de_uso import ConsultarReservas, ObterReserva
from reservas.application.repositorio import FiltrosDeReservas
from reservas.domain.ator import Ator, PapelDoAtor
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
GESTOR = Ator(usuario_id=1, nome="Gestora de Teste", papel=PapelDoAtor.GESTOR)
ATOR_ANA = Ator(usuario_id=ANA.usuario_id, nome=ANA.nome, papel=PapelDoAtor.SOLICITANTE)
QUADRA = 1
CAMPO = 2
ID_INEXISTENTE = 9999


@pytest.fixture
def repositorio():
    return RepositorioReservasEmMemoria()


@pytest.fixture
def ids(repositorio):
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
    reservas = ConsultarReservas(repositorio).executar(FiltrosDeReservas(), ator=GESTOR)

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
    reservas = ConsultarReservas(repositorio).executar(filtros, ator=GESTOR)

    # Assert
    assert _ids_de(reservas) == _ids_de(repositorio.listar(filtros))


def test_consultar_combina_os_filtros(repositorio, ids):
    # Act
    reservas = ConsultarReservas(repositorio).executar(
        FiltrosDeReservas(espaco_id=QUADRA, solicitante="bruno"), ator=GESTOR
    )

    # Assert
    assert _ids_de(reservas) == [ids["meio_dia"]]


def test_obter_devolve_a_reserva(repositorio, ids):
    # Act
    reserva = ObterReserva(repositorio).executar(ids["tarde"], ator=GESTOR)

    # Assert
    assert reserva.id == ids["tarde"]
    assert reserva.solicitante == ANA
    assert reserva.espaco_id == QUADRA


def test_obter_id_inexistente_lanca_reserva_nao_encontrada(repositorio):
    # Act / Assert
    with pytest.raises(ReservaNaoEncontrada) as erro:
        ObterReserva(repositorio).executar(ID_INEXISTENTE, ator=GESTOR)

    assert erro.value.reserva_id == ID_INEXISTENTE
    assert erro.value.mensagem == f"Reserva de código {ID_INEXISTENTE} não encontrada."


@pytest.mark.parametrize(
    "filtros",
    [
        FiltrosDeReservas(),
        FiltrosDeReservas(solicitante_usuario_id=BRUNO.usuario_id),
        FiltrosDeReservas(solicitante="bruno"),
    ],
    ids=["sem-filtros", "usuario-de-outro", "nome-de-outro"],
)
def test_solicitante_so_ve_as_proprias_mesmo_filtrando_por_outro(
    repositorio, ids, filtros
):
    # Act
    reservas = ConsultarReservas(repositorio).executar(filtros, ator=ATOR_ANA)

    # Assert
    assert all(reserva.solicitante == ANA for reserva in reservas)
    assert ids["meio_dia"] not in _ids_de(reservas)


def test_solicitante_sem_filtros_ve_todas_as_proprias(repositorio, ids):
    # Act
    reservas = ConsultarReservas(repositorio).executar(
        FiltrosDeReservas(), ator=ATOR_ANA
    )

    # Assert
    assert _ids_de(reservas) == [ids["tarde"]]


def test_gestor_ve_todas_e_filtra_por_solicitante(repositorio, ids):
    # Act
    todas = ConsultarReservas(repositorio).executar(FiltrosDeReservas(), ator=GESTOR)
    do_bruno = ConsultarReservas(repositorio).executar(
        FiltrosDeReservas(solicitante="bruno"), ator=GESTOR
    )

    # Assert
    assert len(todas) == 3
    assert _ids_de(do_bruno) == [ids["manha"], ids["meio_dia"]]


def test_obter_reserva_de_outra_pessoa_como_solicitante_lanca_nao_encontrada(
    repositorio, ids
):
    # Act / Assert
    with pytest.raises(ReservaNaoEncontrada) as erro:
        ObterReserva(repositorio).executar(ids["manha"], ator=ATOR_ANA)

    assert erro.value.reserva_id == ids["manha"]


def test_obter_a_propria_reserva_como_solicitante(repositorio, ids):
    # Act
    reserva = ObterReserva(repositorio).executar(ids["tarde"], ator=ATOR_ANA)

    # Assert
    assert reserva.solicitante == ANA
