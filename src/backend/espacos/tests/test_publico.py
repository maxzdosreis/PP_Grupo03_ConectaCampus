from dataclasses import FrozenInstanceError

import pytest

from espacos import publico
from espacos.domain.excecoes import EspacoInativo, EspacoNaoEncontrado
from espacos.infrastructure.repositorio_django import RepositorioEspacosDjango
from espacos.tests.fakes import ID_INEXISTENTE, novo_espaco

pytestmark = pytest.mark.django_db


def _salvar(nome="Ginásio A", *, ativo=True):
    return RepositorioEspacosDjango().salvar(novo_espaco(nome=nome, ativo=ativo))


def test_verificar_espaco_disponivel_devolve_dto_com_id_e_nome():
    # Arrange
    salvo = _salvar("Ginásio Central")

    # Act
    disponivel = publico.verificar_espaco_disponivel(salvo.id)

    # Assert
    assert disponivel == publico.EspacoDisponivel(
        id=salvo.id,
        nome="Ginásio Central",
        abertura="07:00",
        fechamento="00:00",
        abertura_em_minutos=7 * 60,
        fechamento_em_minutos=24 * 60,
    )


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


def test_sem_consulta_de_reservas_registrada_e_erro_de_configuracao(monkeypatch):
    # Arrange
    from django.core.exceptions import ImproperlyConfigured

    from espacos.infrastructure import consulta_de_reservas

    monkeypatch.setattr(consulta_de_reservas, "_registrada", None)

    # Act / Assert
    with pytest.raises(ImproperlyConfigured, match="Nenhuma consulta de reservas"):
        consulta_de_reservas.consulta_registrada()


def test_nomes_dos_espacos_devolve_o_nome_de_cada_id_inclusive_de_inativos():
    # Arrange
    ativo = _salvar("Ginásio Central")
    inativo = _salvar("Campo Velho", ativo=False)

    # Act
    nomes = publico.nomes_dos_espacos([ativo.id, inativo.id, ID_INEXISTENTE])

    # Assert
    assert dict(nomes) == {ativo.id: "Ginásio Central", inativo.id: "Campo Velho"}
