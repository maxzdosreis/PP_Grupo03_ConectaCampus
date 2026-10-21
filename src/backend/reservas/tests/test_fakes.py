import pytest

from compartilhado.domain.erros import ConflitoDeEstado, RecursoNaoEncontrado
from reservas.application.portas import EspacoReservavel
from reservas.tests.fakes import ConsultaDeEspacosEmMemoria

QUADRA = EspacoReservavel(id=1, nome="Quadra Coberta")
GINASIO_ANTIGO = EspacoReservavel(id=2, nome="Ginásio Antigo")
ID_INEXISTENTE = 9999


@pytest.fixture
def consulta():
    return ConsultaDeEspacosEmMemoria(
        [QUADRA, GINASIO_ANTIGO], ids_inativos=[GINASIO_ANTIGO.id]
    )


def test_espaco_conhecido_e_ativo_e_devolvido(consulta):
    # Act
    espaco = consulta.obter_espaco_reservavel(QUADRA.id)

    # Assert
    assert espaco == QUADRA


def test_espaco_desconhecido_lanca_recurso_nao_encontrado(consulta):
    # Act
    with pytest.raises(RecursoNaoEncontrado) as erro:
        consulta.obter_espaco_reservavel(ID_INEXISTENTE)

    # Assert
    assert erro.value.mensagem == f"Espaço de código {ID_INEXISTENTE} não encontrado."


def test_espaco_inativo_lanca_conflito_de_estado(consulta):
    # Act / Assert
    with pytest.raises(ConflitoDeEstado):
        consulta.obter_espaco_reservavel(GINASIO_ANTIGO.id)
