from datetime import time, timedelta

import pytest

from compartilhado.api.tratador_de_erros import tratar_excecao
from reservas.domain.conflito_de_horario import garantir_horario_livre
from reservas.domain.excecoes import ConflitoDeHorario
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import (
    BRUNO,
    DIA,
    intervalo,
    reserva_reconstituida,
    reserva_solicitada,
)

S = SituacaoReserva
MENSAGEM_CONFIRMADA_10_AS_11 = (
    "Este espaço já tem uma reserva Confirmada em 25/10/2026 10:00–11:00. "
    "Escolha outro horário."
)


def _nova(**sobrescritas):
    return reserva_solicitada(**sobrescritas)


def _existente(
    *,
    id=50,
    espaco_id=3,
    hora_inicio=time(10, 0),
    hora_fim=time(11, 0),
    data=DIA,
    situacao=S.CONFIRMADA,
):
    return reserva_reconstituida(
        id=id,
        espaco_id=espaco_id,
        solicitante=BRUNO,
        intervalo=IntervaloDeHorario(
            data=data, hora_inicio=hora_inicio, hora_fim=hora_fim
        ),
        finalidade="Aula de educação física",
        situacao=situacao,
    )


def test_sem_reservas_existentes_o_horario_esta_livre():
    # Act / Assert
    garantir_horario_livre(_nova(), [])


@pytest.mark.parametrize("situacao", [S.SOLICITADA, S.CONFIRMADA])
def test_sobreposicao_com_reserva_que_ocupa_horario_e_conflito(situacao):
    # Arrange
    ocupante = _existente(situacao=situacao)

    # Act
    with pytest.raises(ConflitoDeHorario) as erro:
        garantir_horario_livre(_nova(), [ocupante])

    # Assert
    assert erro.value.situacao is situacao
    assert erro.value.intervalo == ocupante.intervalo


@pytest.mark.parametrize("situacao", [S.RECUSADA, S.CANCELADA, S.CONCLUIDA])
def test_sobreposicao_com_reserva_que_nao_ocupa_horario_e_aceita(situacao):
    # Act / Assert
    garantir_horario_livre(_nova(), [_existente(situacao=situacao)])


def test_mesmo_horario_em_outro_espaco_e_aceito():
    # Act / Assert
    garantir_horario_livre(_nova(espaco_id=3), [_existente(espaco_id=4)])


def test_mesmo_horario_em_outra_data_e_aceito():
    # Act / Assert
    garantir_horario_livre(_nova(), [_existente(data=DIA + timedelta(days=1))])


@pytest.mark.parametrize(
    ("hora_inicio", "hora_fim"),
    [(time(9, 0), time(10, 0)), (time(11, 0), time(12, 0))],
)
def test_horario_encostado_e_aceito(hora_inicio, hora_fim):
    # Arrange
    vizinha = _existente(hora_inicio=hora_inicio, hora_fim=hora_fim)

    # Act / Assert
    garantir_horario_livre(_nova(), [vizinha])


def test_a_propria_reserva_na_lista_nao_conta():
    # Arrange
    gravada = _existente(id=12, situacao=S.SOLICITADA)
    editada = _existente(id=12, situacao=S.SOLICITADA, hora_fim=time(11, 30))

    # Act / Assert
    garantir_horario_livre(editada, [gravada])


def test_reservas_sem_id_nao_sao_tratadas_como_a_mesma():
    # Arrange
    pendente = _nova()

    # Act / Assert
    with pytest.raises(ConflitoDeHorario):
        garantir_horario_livre(_nova(), [pendente])


def test_varias_em_conflito_a_mensagem_cita_a_de_inicio_mais_cedo():
    # Arrange
    nova = _nova(hora_inicio=time(9, 0), hora_fim=time(12, 0))
    existentes = [
        _existente(id=1, hora_inicio=time(11, 0), hora_fim=time(12, 0)),
        _existente(id=2, hora_inicio=time(9, 30), hora_fim=time(10, 0)),
        _existente(id=3, hora_inicio=time(10, 0), hora_fim=time(11, 0)),
    ]

    # Act
    with pytest.raises(ConflitoDeHorario) as erro:
        garantir_horario_livre(nova, existentes)

    # Assert
    assert erro.value.intervalo == existentes[1].intervalo


def test_aceita_qualquer_iteravel_de_reservas():
    # Arrange
    existentes = (reserva for reserva in [_existente()])

    # Act / Assert
    with pytest.raises(ConflitoDeHorario):
        garantir_horario_livre(_nova(), existentes)


def test_mensagem_mostra_horario_e_situacao_sem_dados_do_outro_solicitante():
    # Act
    with pytest.raises(ConflitoDeHorario) as erro:
        garantir_horario_livre(_nova(), [_existente()])

    # Assert
    mensagem = erro.value.mensagem
    assert mensagem == MENSAGEM_CONFIRMADA_10_AS_11
    assert BRUNO.nome not in mensagem
    assert BRUNO.matricula not in mensagem
    assert erro.value.campo is None


def test_conflito_de_horario_vira_409_sem_campos():
    # Arrange
    ocupado = intervalo()

    # Act
    resposta = tratar_excecao(ConflitoDeHorario(ocupado, S.CONFIRMADA), {})

    # Assert
    assert resposta.status_code == 409
    assert resposta.data == {
        "erro": {
            "codigo": "CONFLITO_DE_HORARIO",
            "mensagem": MENSAGEM_CONFIRMADA_10_AS_11,
        }
    }
