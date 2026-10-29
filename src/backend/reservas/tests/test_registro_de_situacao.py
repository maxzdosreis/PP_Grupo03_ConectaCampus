from dataclasses import FrozenInstanceError
from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from reservas.domain.registro_de_situacao import RegistroDeSituacao
from reservas.domain.situacao import SituacaoReserva

S = SituacaoReserva
AGORA = datetime(2026, 10, 21, 12, 0, tzinfo=ZoneInfo("America/Sao_Paulo"))


def _registro(**sobrescritas):
    dados = {
        "situacao_anterior": S.SOLICITADA,
        "situacao_nova": S.CONFIRMADA,
        "motivo": None,
        "autor_usuario_id": 1,
        "autor_nome": "Gestora de Teste",
        "registrado_em": AGORA,
    }
    dados.update(sobrescritas)
    return RegistroDeSituacao(**dados)


def test_registro_valido_guarda_os_fatos():
    # Act
    registro = _registro(motivo="Liberada")

    # Assert
    assert registro.situacao_anterior is S.SOLICITADA
    assert registro.situacao_nova is S.CONFIRMADA
    assert registro.motivo == "Liberada"
    assert (registro.autor_usuario_id, registro.autor_nome) == (1, "Gestora de Teste")
    assert registro.registrado_em == AGORA


def test_registro_de_criacao_nao_tem_situacao_anterior():
    # Act
    registro = _registro(situacao_anterior=None, situacao_nova=S.SOLICITADA)

    # Assert
    assert registro.situacao_anterior is None


def test_registro_e_imutavel():
    # Arrange
    registro = _registro()

    # Act / Assert
    with pytest.raises(FrozenInstanceError):
        registro.situacao_nova = S.CANCELADA


def test_registros_com_os_mesmos_fatos_sao_iguais():
    # Assert
    assert _registro() == _registro()


@pytest.mark.parametrize(
    ("campos", "erro"),
    [
        ({"situacao_nova": None}, TypeError),
        ({"situacao_nova": "CONFIRMADA"}, TypeError),
        ({"situacao_anterior": "SOLICITADA"}, TypeError),
        ({"situacao_anterior": S.CONFIRMADA}, ValueError),
        ({"registrado_em": None}, TypeError),
        ({"registrado_em": datetime(2026, 10, 21, 12, 0)}, TypeError),
        ({"autor_usuario_id": 0}, ValueError),
        ({"autor_usuario_id": True}, ValueError),
        ({"autor_usuario_id": "1"}, ValueError),
        ({"autor_nome": ""}, ValueError),
        ({"autor_nome": "   "}, ValueError),
        ({"autor_nome": None}, ValueError),
    ],
    ids=[
        "nova-ausente",
        "nova-em-texto",
        "anterior-em-texto",
        "anterior-igual-a-nova",
        "sem-registrado-em",
        "registrado-em-sem-fuso",
        "autor-id-zero",
        "autor-id-bool",
        "autor-id-texto",
        "autor-nome-vazio",
        "autor-nome-so-espacos",
        "autor-nome-ausente",
    ],
)
def test_registro_invalido_e_erro_de_programacao(campos, erro):
    # Act / Assert
    with pytest.raises(erro):
        _registro(**campos)
