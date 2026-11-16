"""Contrato do repositório da gestão de usuários: Django e fake se comportam igual."""

import pytest
from django.contrib.auth import get_user_model
from django.db import connection
from django.test.utils import CaptureQueriesContext

from compartilhado.domain.paginacao import Paginacao
from contas.application.portas import FiltrosDeUsuarios
from contas.domain.excecoes import UltimoGestorAtivo, UsuarioNaoEncontrado
from contas.domain.gestao import SituacaoDoUsuario
from contas.domain.perfil import PerfilUsuario
from contas.infrastructure.repositorio_django import RepositorioGestaoDeUsuariosDjango
from contas.tests.fakes import (
    RepositorioGestaoDeUsuariosEmMemoria,
    novo_usuario_gerenciado,
)

GESTOR = PerfilUsuario.GESTOR
SOLICITANTE = PerfilUsuario.SOLICITANTE
SENHA = "Quadra-Azul-2026!"

ANA = "Ana Souza"
BRUNO = "Bruno Lima"
CARLA = "Carla Dias"
DANIEL = "Daniel Reis"
BIANCA = "bianca Alves"

_PESSOAS = [
    (ANA, "A001", GESTOR, True),
    (BRUNO, "B002", SOLICITANTE, True),
    (CARLA, "C003", SOLICITANTE, False),
    (DANIEL, "D004", GESTOR, False),
    (BIANCA, "E005", SOLICITANTE, True),
]


def _para_django():
    modelo = get_user_model()
    for indice, (nome, matricula, perfil, ativo) in enumerate(_PESSOAS, start=1):
        modelo.objects.create_user(
            f"pessoa{indice}@exemplo.com",
            SENHA,
            nome=nome,
            matricula=matricula,
            perfil=perfil.value,
            is_active=ativo,
        )
    return RepositorioGestaoDeUsuariosDjango()


def _para_memoria():
    return RepositorioGestaoDeUsuariosEmMemoria(
        [
            novo_usuario_gerenciado(
                indice, perfil=perfil, ativo=ativo, nome=nome, matricula=matricula
            )
            for indice, (nome, matricula, perfil, ativo) in enumerate(_PESSOAS, start=1)
        ]
    )


@pytest.fixture(
    params=[
        pytest.param(_para_django, marks=pytest.mark.django_db, id="django"),
        pytest.param(_para_memoria, id="memoria"),
    ]
)
def repositorio(request):
    return request.param()


def _nomes(repositorio, filtros=None):
    pagina = repositorio.listar(filtros or FiltrosDeUsuarios(), Paginacao(tamanho=100))
    return [usuario.nome for usuario in pagina.itens]


def _id_de(repositorio, nome):
    pagina = repositorio.listar(FiltrosDeUsuarios(busca=nome), Paginacao(tamanho=100))
    (usuario,) = pagina.itens
    return usuario.id


def _decidir_para(nova):
    return lambda atual, gestores_ativos: nova


def test_listar_ordena_por_nome_em_ordem_de_code_point(repositorio):
    # Act
    pagina = repositorio.listar(FiltrosDeUsuarios(), Paginacao(tamanho=100))

    # Assert: maiúsculas vêm antes de minúsculas
    assert [u.nome for u in pagina.itens] == [ANA, BRUNO, CARLA, DANIEL, BIANCA]
    assert pagina.total == 5


def test_listar_desempata_nomes_iguais_pelo_id(repositorio):
    # Arrange
    if isinstance(repositorio, RepositorioGestaoDeUsuariosEmMemoria):
        repositorio.usuarios[10] = novo_usuario_gerenciado(10, nome=ANA)
        repositorio.usuarios[11] = novo_usuario_gerenciado(11, nome=ANA)
    else:
        for numero in (10, 11):
            get_user_model().objects.create_user(
                f"copia{numero}@exemplo.com",
                SENHA,
                nome=ANA,
                matricula=f"Z{numero}",
            )

    # Act
    pagina = repositorio.listar(FiltrosDeUsuarios(busca=ANA), Paginacao(tamanho=100))

    # Assert
    ids = [usuario.id for usuario in pagina.itens]
    assert len(ids) == 3
    assert ids == sorted(ids)


def test_listar_filtra_por_perfil_e_por_ativo(repositorio):
    # Act / Assert
    assert _nomes(repositorio, FiltrosDeUsuarios(perfil=GESTOR)) == [ANA, DANIEL]
    assert _nomes(repositorio, FiltrosDeUsuarios(ativo=False)) == [CARLA, DANIEL]
    assert _nomes(repositorio, FiltrosDeUsuarios(perfil=GESTOR, ativo=True)) == [ANA]


@pytest.mark.parametrize(
    ("busca", "esperados"),
    [
        ("souza", [ANA]),
        ("BRUNO", [BRUNO]),
        ("pessoa3@", [CARLA]),
        ("pessoa3@exemplo.com", [CARLA]),
        ("e005", [BIANCA]),
        ("inexistente", []),
    ],
)
def test_listar_busca_em_nome_email_e_matricula_sem_diferenciar_caixa(
    repositorio, busca, esperados
):
    # Act / Assert
    assert _nomes(repositorio, FiltrosDeUsuarios(busca=busca)) == esperados


def test_listar_pagina_com_total_certo(repositorio):
    # Act
    primeira = repositorio.listar(FiltrosDeUsuarios(), Paginacao(numero=1, tamanho=2))
    ultima = repositorio.listar(FiltrosDeUsuarios(), Paginacao(numero=3, tamanho=2))

    # Assert
    assert [u.nome for u in primeira.itens] == [ANA, BRUNO]
    assert [u.nome for u in ultima.itens] == [BIANCA]
    assert primeira.total == ultima.total == 5
    assert primeira.total_de_paginas() == 3


def test_pagina_depois_da_ultima_vem_vazia_com_o_total(repositorio):
    # Act
    pagina = repositorio.listar(FiltrosDeUsuarios(), Paginacao(numero=9, tamanho=2))

    # Assert
    assert pagina.itens == ()
    assert pagina.total == 5


def test_listar_sem_resultado_tem_total_zero(repositorio):
    # Act
    pagina = repositorio.listar(
        FiltrosDeUsuarios(busca="nada"), Paginacao(numero=1, tamanho=2)
    )

    # Assert
    assert (pagina.itens, pagina.total, pagina.total_de_paginas()) == ((), 0, 0)


def test_listar_devolve_so_os_dados_da_gestao(repositorio):
    # Act
    usuario = repositorio.listar(
        FiltrosDeUsuarios(busca=ANA), Paginacao(tamanho=100)
    ).itens[0]

    # Assert
    assert usuario.email == "pessoa1@exemplo.com"
    assert usuario.matricula == "A001"
    assert usuario.perfil is GESTOR
    assert usuario.ativo is True
    assert usuario.cadastrado_em is not None
    assert usuario.ultimo_acesso is None
    assert not {"password", "senha", "hash"} & set(vars(usuario))


def test_alterar_usuario_inexistente_lanca_nao_encontrado(repositorio):
    # Act / Assert
    with pytest.raises(UsuarioNaoEncontrado):
        repositorio.alterar_sob_trava(
            999_999, _decidir_para(SituacaoDoUsuario(GESTOR, True))
        )


def test_alterar_grava_a_situacao_nova_e_devolve_o_usuario(repositorio):
    # Arrange
    bruno = _id_de(repositorio, BRUNO)

    # Act
    resultado = repositorio.alterar_sob_trava(
        bruno, _decidir_para(SituacaoDoUsuario(GESTOR, False))
    )

    # Assert
    assert resultado.alterou is True
    assert (resultado.usuario.perfil, resultado.usuario.ativo) == (GESTOR, False)
    assert BRUNO in _nomes(repositorio, FiltrosDeUsuarios(perfil=GESTOR, ativo=False))


def test_alterar_para_a_mesma_situacao_nao_altera(repositorio):
    # Arrange
    bruno = _id_de(repositorio, BRUNO)

    # Act
    resultado = repositorio.alterar_sob_trava(
        bruno, _decidir_para(SituacaoDoUsuario(SOLICITANTE, True))
    )

    # Assert
    assert resultado.alterou is False
    assert resultado.usuario.nome == BRUNO


def test_decidir_recebe_o_usuario_e_a_contagem_de_gestores_ativos(repositorio):
    # Arrange
    bruno = _id_de(repositorio, BRUNO)
    vistos = []

    def decidir(atual, gestores_ativos):
        vistos.append((atual.nome, gestores_ativos))
        return atual.situacao

    # Act
    repositorio.alterar_sob_trava(bruno, decidir)

    # Assert: só a Ana é Gestora ativa (o Daniel está inativo)
    assert vistos == [(BRUNO, 1)]


def test_recusa_do_decidir_nao_grava_nada(repositorio):
    # Arrange
    ana = _id_de(repositorio, ANA)

    def decidir(atual, gestores_ativos):
        raise UltimoGestorAtivo

    # Act
    with pytest.raises(UltimoGestorAtivo):
        repositorio.alterar_sob_trava(ana, decidir)

    # Assert
    assert _nomes(repositorio, FiltrosDeUsuarios(perfil=GESTOR, ativo=True)) == [ANA]


@pytest.mark.django_db
def test_alterar_trava_o_alvo_e_os_gestores_ativos_em_ordem_de_id():
    # Arrange
    repositorio = _para_django()
    bruno = _id_de(repositorio, BRUNO)

    # Act
    with CaptureQueriesContext(connection) as consultas:
        repositorio.alterar_sob_trava(bruno, lambda atual, _: atual.situacao)

    # Assert
    travas = [c["sql"] for c in consultas if "FOR UPDATE" in c["sql"]]
    assert len(travas) == 1
    assert 'ORDER BY "contas_usuario"."id"' in travas[0]


@pytest.mark.django_db
def test_listar_depois_do_fim_so_conta():
    # Arrange
    repositorio = _para_django()

    # Act
    with CaptureQueriesContext(connection) as consultas:
        repositorio.listar(FiltrosDeUsuarios(), Paginacao(numero=9, tamanho=2))

    # Assert
    assert len(consultas) == 1
    assert "COUNT" in consultas[0]["sql"]


@pytest.mark.django_db
def test_listar_faz_count_e_a_pagina_com_limit_offset():
    # Arrange
    repositorio = _para_django()

    # Act
    with CaptureQueriesContext(connection) as consultas:
        repositorio.listar(FiltrosDeUsuarios(), Paginacao(numero=2, tamanho=2))

    # Assert
    assert len(consultas) == 2
    assert "LIMIT 2 OFFSET 2" in consultas[1]["sql"]
