from dataclasses import FrozenInstanceError

import pytest

from espacos import publico
from espacos.domain.espaco_esportivo import EspacoEsportivo
from espacos.domain.excecoes import EspacoInativo, EspacoNaoEncontrado
from espacos.domain.tipo_espaco import TipoEspaco
from espacos.infrastructure.repositorio_django import RepositorioEspacosDjango

pytestmark = pytest.mark.django_db

ID_INEXISTENTE = 9999


def _salvar(nome="Ginásio A", *, ativo=True):
    return RepositorioEspacosDjango().salvar(
        EspacoEsportivo(nome=nome, tipo=TipoEspaco.GINASIO, capacidade=10, ativo=ativo)
    )


def test_verificar_espaco_disponivel_devolve_dto_com_id_e_nome():
    # Arrange
    salvo = _salvar("Ginásio Central")

    # Act
    disponivel = publico.verificar_espaco_disponivel(salvo.id)

    # Assert
    assert disponivel == publico.EspacoDisponivel(id=salvo.id, nome="Ginásio Central")


def test_espaco_disponivel_e_imutavel():
    # Arrange
    disponivel = publico.verificar_espaco_disponivel(_salvar().id)

    # Act / Assert
    with pytest.raises(FrozenInstanceError):
        disponivel.nome = "Outro nome"


def test_verificar_espaco_inexistente_lanca_espaco_nao_encontrado():
    # Act
    with pytest.raises(EspacoNaoEncontrado) as erro:
        publico.verificar_espaco_disponivel(ID_INEXISTENTE)

    # Assert
    assert erro.value.espaco_id == ID_INEXISTENTE


def test_verificar_espaco_inativo_lanca_espaco_inativo():
    # Arrange
    inativo = _salvar("Ginásio Antigo", ativo=False)

    # Act / Assert
    with pytest.raises(EspacoInativo):
        publico.verificar_espaco_disponivel(inativo.id)
