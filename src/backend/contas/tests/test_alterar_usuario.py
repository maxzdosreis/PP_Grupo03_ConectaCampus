import pytest

from compartilhado.domain.paginacao import Paginacao
from contas.application.casos_de_uso import AlterarUsuario, ListarUsuarios
from contas.application.portas import FiltrosDeUsuarios
from contas.domain.excecoes import (
    NaoPodeDesativarASiMesmo,
    NaoPodeRebaixarASiMesmo,
    NenhumaAlteracaoNoUsuario,
    UltimoGestorAtivo,
    UsuarioNaoEncontrado,
)
from contas.domain.perfil import PerfilUsuario
from contas.tests.fakes import (
    RepositorioGestaoDeUsuariosEmMemoria,
    novo_usuario_gerenciado,
)

GESTOR = PerfilUsuario.GESTOR
SOLICITANTE = PerfilUsuario.SOLICITANTE
CARLA = 1
OUTRA_GESTORA = 2
BRUNO = 3


def _repositorio(**situacoes):
    carla = novo_usuario_gerenciado(CARLA, perfil=GESTOR, nome="Carla")
    outra = novo_usuario_gerenciado(
        OUTRA_GESTORA,
        perfil=GESTOR,
        ativo=situacoes.get("outra_ativa", True),
        nome="Outra Gestora",
    )
    bruno = novo_usuario_gerenciado(
        BRUNO, ativo=situacoes.get("bruno_ativo", True), nome="Bruno"
    )
    return RepositorioGestaoDeUsuariosEmMemoria([carla, outra, bruno])


def _alterar(repositorio, alvo, *, ator=CARLA, perfil=None, ativo=None):
    return AlterarUsuario(repositorio).executar(
        usuario_id=alvo, ator_id=ator, perfil=perfil, ativo=ativo
    )


def test_sem_perfil_nem_ativo_lanca_nenhuma_alteracao_informada_sem_consultar():
    # Arrange
    repositorio = _repositorio()

    # Act / Assert
    with pytest.raises(NenhumaAlteracaoNoUsuario) as erro:
        _alterar(repositorio, BRUNO)
    assert erro.value.codigo == "NENHUMA_ALTERACAO_INFORMADA"
    assert repositorio.gestores_contados == []


def test_usuario_inexistente_lanca_nao_encontrado():
    # Act / Assert
    with pytest.raises(UsuarioNaoEncontrado) as erro:
        _alterar(_repositorio(), 999, ativo=False)
    assert erro.value.codigo == "USUARIO_NAO_ENCONTRADO"


def test_existencia_vem_antes_das_regras_do_proprio_ator():
    # Arrange: o id do ator não existe no repositório
    repositorio = RepositorioGestaoDeUsuariosEmMemoria([])

    # Act / Assert
    with pytest.raises(UsuarioNaoEncontrado):
        _alterar(repositorio, CARLA, perfil=SOLICITANTE)


def test_promover_solicitante_grava_e_devolve_o_usuario_alterado():
    # Arrange
    repositorio = _repositorio()

    # Act
    resultado = _alterar(repositorio, BRUNO, perfil=GESTOR)

    # Assert
    assert resultado.alterou is True
    assert resultado.usuario.perfil is GESTOR
    assert repositorio.usuarios[BRUNO].perfil is GESTOR
    assert repositorio.chamadas_de_gravar == 1


def test_desativar_e_reativar_um_solicitante():
    # Arrange
    repositorio = _repositorio()

    # Act
    desativado = _alterar(repositorio, BRUNO, ativo=False)
    reativado = _alterar(repositorio, BRUNO, ativo=True)

    # Assert
    assert desativado.usuario.ativo is False
    assert reativado.usuario.ativo is True
    assert repositorio.usuarios[BRUNO].ativo is True


def test_perfil_e_ativo_podem_mudar_juntos():
    # Act
    resultado = _alterar(_repositorio(), BRUNO, perfil=GESTOR, ativo=False)

    # Assert
    assert (resultado.usuario.perfil, resultado.usuario.ativo) == (GESTOR, False)


def test_pedir_o_estado_atual_e_idempotente_e_nao_grava():
    # Arrange
    repositorio = _repositorio()

    # Act
    resultado = _alterar(repositorio, BRUNO, perfil=SOLICITANTE, ativo=True)

    # Assert
    assert resultado.alterou is False
    assert resultado.usuario == repositorio.usuarios[BRUNO]
    assert repositorio.chamadas_de_gravar == 0


def test_gestor_nao_se_rebaixa_nem_se_desativa():
    # Arrange
    repositorio = _repositorio()

    # Act / Assert
    with pytest.raises(NaoPodeRebaixarASiMesmo):
        _alterar(repositorio, CARLA, perfil=SOLICITANTE)
    with pytest.raises(NaoPodeDesativarASiMesmo):
        _alterar(repositorio, CARLA, ativo=False)
    assert repositorio.usuarios[CARLA].situacao.eh_gestor_ativo
    assert repositorio.chamadas_de_gravar == 0


def test_gestor_pode_rebaixar_outro_gestor_havendo_dois_ativos():
    # Arrange
    repositorio = _repositorio()

    # Act
    resultado = _alterar(repositorio, OUTRA_GESTORA, perfil=SOLICITANTE)

    # Assert
    assert resultado.usuario.perfil is SOLICITANTE


def test_conta_dos_gestores_ativos_chega_ao_dominio_como_a_do_repositorio():
    # Arrange
    repositorio = _repositorio()

    # Act
    _alterar(repositorio, BRUNO, ativo=False)

    # Assert
    assert repositorio.gestores_contados == [2]


def test_rebaixar_o_ultimo_gestor_ativo_e_recusado_e_nada_muda():
    # Arrange
    repositorio = _repositorio(outra_ativa=False)
    bruno_promovido = _alterar(repositorio, BRUNO, perfil=GESTOR)
    assert bruno_promovido.alterou
    _alterar(repositorio, BRUNO, ativo=False)

    # Act / Assert
    with pytest.raises(UltimoGestorAtivo):
        _alterar(repositorio, CARLA, ator=BRUNO, perfil=SOLICITANTE)
    with pytest.raises(UltimoGestorAtivo):
        _alterar(repositorio, CARLA, ator=BRUNO, ativo=False)
    assert repositorio.usuarios[CARLA].situacao.eh_gestor_ativo


def test_promover_ou_reativar_e_permitido_sem_nenhum_gestor_ativo_alem_do_alvo():
    # Arrange
    repositorio = _repositorio(outra_ativa=False)

    # Act
    reativada = _alterar(repositorio, OUTRA_GESTORA, ativo=True)

    # Assert
    assert reativada.usuario.ativo is True


def test_listar_repassa_filtros_e_paginacao_ao_repositorio():
    # Arrange
    caso = ListarUsuarios(_repositorio())

    # Act
    pagina = caso.executar(
        FiltrosDeUsuarios(perfil=GESTOR), Paginacao(numero=1, tamanho=1)
    )

    # Assert
    assert pagina.total == 2
    assert [u.nome for u in pagina.itens] == ["Carla"]
    assert pagina.total_de_paginas() == 2
