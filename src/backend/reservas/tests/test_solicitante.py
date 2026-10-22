from dataclasses import FrozenInstanceError

import pytest

from compartilhado.domain.erros import CampoObrigatorioAusente
from reservas.domain.solicitante import Solicitante


def _criar_solicitante(**sobrescritas):
    dados = {"usuario_id": 7, "nome": "Ana Souza", "matricula": "2026001"}
    dados.update(sobrescritas)
    return Solicitante(**dados)


def test_criacao_valida_normaliza_nome_e_matricula():
    # Act
    solicitante = _criar_solicitante(nome="  Ana   Souza ", matricula=" 2026 001 ")

    # Assert
    assert solicitante.usuario_id == 7
    assert solicitante.nome == "Ana Souza"
    assert solicitante.matricula == "2026 001"


@pytest.mark.parametrize(
    ("campo", "valor"),
    [
        ("usuario_id", None),
        ("nome", None),
        ("nome", ""),
        ("nome", "   "),
        ("matricula", None),
        ("matricula", ""),
        ("matricula", "   "),
    ],
)
def test_campo_vazio_e_recusado_como_obrigatorio(campo, valor):
    # Act
    with pytest.raises(CampoObrigatorioAusente) as erro:
        _criar_solicitante(**{campo: valor})

    # Assert
    assert erro.value.campo == campo


@pytest.mark.parametrize("usuario_id", [0, -1, True, "1"])
def test_usuario_id_que_nao_e_inteiro_positivo_e_erro_de_programacao(usuario_id):
    # Act / Assert
    with pytest.raises(ValueError, match="inteiro positivo"):
        _criar_solicitante(usuario_id=usuario_id)


def test_solicitante_e_imutavel():
    # Arrange
    solicitante = _criar_solicitante()

    # Act / Assert
    with pytest.raises(FrozenInstanceError):
        solicitante.nome = "Outro"


def test_solicitantes_com_mesmos_dados_sao_iguais():
    # Assert
    assert _criar_solicitante() == _criar_solicitante(nome=" Ana  Souza")
