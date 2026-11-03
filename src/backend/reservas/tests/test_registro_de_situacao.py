from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from reservas.domain.registro_de_situacao import RegistroDeSituacao
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import AGORA, exatamente

S = SituacaoReserva


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


_NOVA_INVALIDA = "situacao_nova deve ser uma SituacaoReserva."
_ANTERIOR_INVALIDA = "situacao_anterior deve ser uma SituacaoReserva ou None."
_ANTERIOR_IGUAL = "situacao_anterior deve ser diferente de situacao_nova."
_SEM_FUSO = "registrado_em deve ser um datetime com fuso horário."
_AUTOR_ID = "autor_usuario_id deve ser um inteiro positivo."
_AUTOR_NOME = "autor_nome é obrigatório."


@pytest.mark.parametrize(
    ("campos", "erro", "mensagem"),
    [
        ({"situacao_nova": None}, TypeError, _NOVA_INVALIDA),
        ({"situacao_nova": "CONFIRMADA"}, TypeError, _NOVA_INVALIDA),
        ({"situacao_anterior": "SOLICITADA"}, TypeError, _ANTERIOR_INVALIDA),
        ({"situacao_anterior": S.CONFIRMADA}, ValueError, _ANTERIOR_IGUAL),
        ({"registrado_em": None}, TypeError, _SEM_FUSO),
        ({"registrado_em": datetime(2026, 10, 21, 12, 0)}, TypeError, _SEM_FUSO),
        ({"autor_usuario_id": 0}, ValueError, _AUTOR_ID),
        ({"autor_usuario_id": True}, ValueError, _AUTOR_ID),
        ({"autor_usuario_id": "1"}, ValueError, _AUTOR_ID),
        ({"autor_nome": ""}, ValueError, _AUTOR_NOME),
        ({"autor_nome": "   "}, ValueError, _AUTOR_NOME),
        ({"autor_nome": None}, ValueError, _AUTOR_NOME),
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
def test_registro_invalido_e_erro_de_programacao(campos, erro, mensagem):
    # Act / Assert
    with pytest.raises(erro, match=exatamente(mensagem)):
        _registro(**campos)
