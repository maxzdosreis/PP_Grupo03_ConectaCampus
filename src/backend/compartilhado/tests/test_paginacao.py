import pytest
from django.http import QueryDict
from rest_framework.exceptions import ValidationError

from compartilhado.api.paginacao import (
    FiltrosDePaginaSerializer,
    PaginacaoSaidaSerializer,
)
from compartilhado.domain.paginacao import (
    TAMANHO_MAXIMO_DA_PAGINA,
    TAMANHO_PADRAO_DA_PAGINA,
    Paginacao,
    PaginaDeItens,
)


def test_paginacao_padrao_e_a_primeira_pagina_de_vinte():
    # Act
    paginacao = Paginacao()

    # Assert
    assert (paginacao.numero, paginacao.tamanho) == (1, TAMANHO_PADRAO_DA_PAGINA)
    assert TAMANHO_PADRAO_DA_PAGINA == 20
    assert TAMANHO_MAXIMO_DA_PAGINA == 100


@pytest.mark.parametrize(
    ("numero", "tamanho", "esperado"), [(1, 20, 0), (2, 20, 20), (3, 5, 10)]
)
def test_deslocamento_pula_as_paginas_anteriores(numero, tamanho, esperado):
    # Act / Assert
    assert Paginacao(numero=numero, tamanho=tamanho).deslocamento() == esperado


@pytest.mark.parametrize("numero", [0, -1])
def test_numero_menor_que_um_e_erro_de_programacao(numero):
    # Act / Assert
    with pytest.raises(ValueError, match="O número da página deve ser 1 ou maior."):
        Paginacao(numero=numero)


@pytest.mark.parametrize("tamanho", [0, 101])
def test_tamanho_fora_do_limite_e_erro_de_programacao(tamanho):
    # Act / Assert
    with pytest.raises(ValueError, match="entre 1 e 100"):
        Paginacao(tamanho=tamanho)


@pytest.mark.parametrize("valor", [True, "2", 1.5, None])
def test_numero_e_tamanho_precisam_ser_inteiros(valor):
    # Act / Assert
    with pytest.raises(TypeError, match="deve ser int"):
        Paginacao(numero=valor)
    with pytest.raises(TypeError, match="deve ser int"):
        Paginacao(tamanho=valor)


@pytest.mark.parametrize(
    ("total", "tamanho", "paginas"), [(0, 20, 0), (1, 20, 1), (20, 20, 1), (21, 20, 2)]
)
def test_total_de_paginas_arredonda_para_cima(total, tamanho, paginas):
    # Arrange
    pagina = PaginaDeItens(
        itens=(), total=total, paginacao=Paginacao(numero=1, tamanho=tamanho)
    )

    # Act / Assert
    assert pagina.total_de_paginas() == paginas


def _filtros(dados):
    serializer = FiltrosDePaginaSerializer(data=dados)
    serializer.is_valid(raise_exception=True)
    return serializer


def test_serializer_sem_parametros_usa_a_primeira_pagina_do_tamanho_padrao():
    # Act
    paginacao = _filtros({}).para_paginacao()

    # Assert
    assert paginacao == Paginacao(numero=1, tamanho=20)


def test_serializer_em_branco_vale_o_padrao():
    # Act
    consulta = QueryDict("pagina=&tamanho=")
    paginacao = _filtros(consulta).para_paginacao()

    # Assert
    assert paginacao == Paginacao()


def test_serializer_le_pagina_e_tamanho():
    # Act
    paginacao = _filtros({"pagina": "3", "tamanho": "100"}).para_paginacao()

    # Assert
    assert paginacao == Paginacao(numero=3, tamanho=100)


@pytest.mark.parametrize(
    "dados", [{"pagina": "0"}, {"pagina": "abc"}, {"tamanho": "0"}, {"tamanho": "101"}]
)
def test_serializer_recusa_pagina_e_tamanho_invalidos(dados):
    # Act / Assert
    with pytest.raises(ValidationError):
        _filtros(dados)


def test_saida_traz_pagina_tamanho_total_e_total_de_paginas():
    # Arrange
    pagina = PaginaDeItens(
        itens=("a",), total=41, paginacao=Paginacao(numero=2, tamanho=20)
    )

    # Act
    saida = PaginacaoSaidaSerializer(pagina).data

    # Assert
    assert dict(saida) == {
        "pagina": 2,
        "tamanho": 20,
        "total": 41,
        "total_de_paginas": 3,
    }
