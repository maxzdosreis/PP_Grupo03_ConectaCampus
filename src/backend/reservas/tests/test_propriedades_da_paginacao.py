from datetime import time, timedelta

import pytest
from hypothesis import given
from hypothesis import strategies as st

from reservas.application.repositorio import (
    TAMANHO_MAXIMO_DA_PAGINA,
    TAMANHO_PADRAO_DA_PAGINA,
    FiltrosDeReservas,
    Paginacao,
    PaginaDeReservas,
)
from reservas.tests.fakes import (
    DIA,
    RepositorioReservasEmMemoria,
    exatamente,
    reserva_solicitada,
)

_ESPACOS = (1, 2, 3)
_HORAS = range(8, 12)
_DIAS = range(3)

_vagas = st.lists(
    st.tuples(
        st.sampled_from(_ESPACOS), st.sampled_from(_DIAS), st.sampled_from(_HORAS)
    ),
    unique=True,
    max_size=len(_ESPACOS) * len(_DIAS) * len(_HORAS),
)
_tamanhos = st.one_of(st.integers(1, 12), st.sampled_from([TAMANHO_MAXIMO_DA_PAGINA]))


def _repositorio_com(vagas):
    repositorio = RepositorioReservasEmMemoria()
    for espaco_id, dia, hora in vagas:
        repositorio.salvar(
            reserva_solicitada(
                espaco_id=espaco_id,
                data=DIA + timedelta(days=dia),
                hora_inicio=time(hora),
                hora_fim=time(hora, 30),
            )
        )
    return repositorio


def _chave(reserva):
    return (reserva.intervalo.inicio(), reserva.id)


@given(vagas=_vagas, tamanho=_tamanhos)
def test_as_paginas_em_ordem_formam_a_lista_completa_sem_repeticao(vagas, tamanho):
    # Arrange
    repositorio = _repositorio_com(vagas)

    # Act
    primeira = repositorio.listar(FiltrosDeReservas(), Paginacao(1, tamanho))
    paginas = [
        repositorio.listar(FiltrosDeReservas(), Paginacao(numero, tamanho))
        for numero in range(1, primeira.total_de_paginas() + 2)
    ]

    # Assert
    juntas = [reserva for pagina in paginas for reserva in pagina.itens]
    ids = [reserva.id for reserva in juntas]
    assert len(ids) == len(set(ids)) == len(vagas)
    assert [_chave(reserva) for reserva in juntas] == sorted(map(_chave, juntas))
    assert all(pagina.total == len(vagas) for pagina in paginas)
    assert primeira.total_de_paginas() == -(-len(vagas) // tamanho)
    assert all(len(pagina.itens) == tamanho for pagina in paginas[:-2])
    assert paginas[-1].itens == ()


@given(
    total=st.integers(0, 10**6),
    tamanho=st.integers(1, TAMANHO_MAXIMO_DA_PAGINA),
    numero=st.integers(1, 10**6),
)
def test_total_de_paginas_e_o_menor_numero_que_cobre_o_total(total, tamanho, numero):
    # Act
    pagina = PaginaDeReservas(
        itens=(), total=total, paginacao=Paginacao(numero, tamanho)
    )
    paginas = pagina.total_de_paginas()

    # Assert
    assert paginas * tamanho >= total
    assert (paginas - 1) * tamanho < total or paginas == 0
    assert Paginacao(numero, tamanho).deslocamento() == (numero - 1) * tamanho


def test_paginacao_sem_argumentos_e_a_primeira_pagina_de_tamanho_padrao():
    # Act
    paginacao = Paginacao()

    # Assert
    assert (paginacao.numero, paginacao.tamanho) == (1, TAMANHO_PADRAO_DA_PAGINA)
    assert (TAMANHO_PADRAO_DA_PAGINA, TAMANHO_MAXIMO_DA_PAGINA) == (20, 100)
    assert paginacao.deslocamento() == 0


@pytest.mark.parametrize(
    ("numero", "tamanho"),
    [(1, 1), (1, TAMANHO_MAXIMO_DA_PAGINA), (10**30, 20)],
    ids=["menores", "tamanho-maximo", "numero-enorme"],
)
def test_paginacao_aceita_os_limites(numero, tamanho):
    # Act
    paginacao = Paginacao(numero=numero, tamanho=tamanho)

    # Assert
    assert (paginacao.numero, paginacao.tamanho) == (numero, tamanho)


@pytest.mark.parametrize(
    ("numero", "tamanho", "mensagem"),
    [
        (0, 20, "O número da página deve ser 1 ou maior."),
        (-3, 20, "O número da página deve ser 1 ou maior."),
        (1, 0, "O tamanho da página deve ficar entre 1 e 100."),
        (
            1,
            TAMANHO_MAXIMO_DA_PAGINA + 1,
            "O tamanho da página deve ficar entre 1 e 100.",
        ),
    ],
    ids=["numero-zero", "numero-negativo", "tamanho-zero", "tamanho-acima-do-maximo"],
)
def test_paginacao_fora_dos_limites_e_erro_de_programacao(numero, tamanho, mensagem):
    # Act / Assert
    with pytest.raises(ValueError, match=exatamente(mensagem)):
        Paginacao(numero=numero, tamanho=tamanho)


@pytest.mark.parametrize(
    ("numero", "tamanho", "mensagem"),
    [
        ("1", 20, "numero da paginação deve ser int, recebido '1'."),
        (True, 20, "numero da paginação deve ser int, recebido True."),
        (1, 2.0, "tamanho da paginação deve ser int, recebido 2.0."),
        (1, None, "tamanho da paginação deve ser int, recebido None."),
    ],
    ids=["numero-texto", "numero-bool", "tamanho-float", "tamanho-none"],
)
def test_paginacao_com_tipo_errado_e_erro_de_programacao(numero, tamanho, mensagem):
    # Act / Assert
    with pytest.raises(TypeError, match=exatamente(mensagem)):
        Paginacao(numero=numero, tamanho=tamanho)
