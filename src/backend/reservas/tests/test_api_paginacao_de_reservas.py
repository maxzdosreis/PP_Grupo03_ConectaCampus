from datetime import time, timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from reservas.domain.reserva import Reserva
from reservas.domain.solicitante import Solicitante
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango

pytestmark = pytest.mark.django_db

URL_RESERVAS = reverse("reservas:lista")
TOTAL_DA_MASSA = 25
DO_SOLICITANTE = 9


def _solicitante_de(usuario):
    return Solicitante(
        usuario_id=usuario.pk, nome=usuario.nome, matricula=usuario.matricula
    )


@pytest.fixture
def massa(usuario_solicitante, outro_solicitante, espaco_id):
    repositorio = RepositorioReservasDjango()
    agora = timezone.now()
    amanha = timezone.localdate() + timedelta(days=1)
    ids = []
    for indice in range(TOTAL_DA_MASSA):
        dia, hora = divmod(indice, 10)
        dono = usuario_solicitante
        if indice % 2 or indice > 2 * (DO_SOLICITANTE - 1):
            dono = outro_solicitante
        reserva = Reserva.solicitar(
            espaco_id=espaco_id,
            solicitante=_solicitante_de(dono),
            data=amanha + timedelta(days=dia),
            hora_inicio=time(8 + hora),
            hora_fim=time(9 + hora),
            finalidade=f"Treino {indice:02d}",
            agora=agora,
        )
        ids.append(repositorio.salvar(reserva).id)
    return ids


def _consultar(cliente, parametros=None):
    return cliente.get(URL_RESERVAS, parametros or {})


def _ids_de(resposta):
    return [reserva["id"] for reserva in resposta.data["dados"]]


def test_sem_parametros_devolve_a_primeira_pagina_de_20_com_o_total(
    cliente_gestor, massa
):
    # Act
    resposta = _consultar(cliente_gestor)

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "25 reservas encontradas."
    assert _ids_de(resposta) == massa[:20]
    assert resposta.data["paginacao"] == {
        "pagina": 1,
        "tamanho": 20,
        "total": 25,
        "total_de_paginas": 2,
    }


def test_pagina_e_tamanho_escolhem_o_trecho_na_ordem_por_inicio(cliente_gestor, massa):
    # Act
    resposta = _consultar(cliente_gestor, {"tamanho": 2, "pagina": 2})

    # Assert
    assert resposta.status_code == 200
    assert _ids_de(resposta) == massa[2:4]
    assert resposta.data["paginacao"] == {
        "pagina": 2,
        "tamanho": 2,
        "total": 25,
        "total_de_paginas": 13,
    }


def test_as_paginas_juntas_dao_a_lista_completa_sem_repeticao(cliente_gestor, massa):
    # Act
    paginas = [
        _consultar(cliente_gestor, {"tamanho": 7, "pagina": numero})
        for numero in (1, 2, 3, 4)
    ]

    # Assert
    assert [len(_ids_de(pagina)) for pagina in paginas] == [7, 7, 7, 4]
    assert [id_ for pagina in paginas for id_ in _ids_de(pagina)] == massa


@pytest.mark.parametrize("pagina", [3, 99, 10**30], ids=["seguinte", "99", "enorme"])
def test_pagina_depois_da_ultima_responde_200_sem_reservas(
    cliente_gestor, massa, pagina
):
    # Act
    resposta = _consultar(cliente_gestor, {"pagina": pagina})

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["dados"] == []
    assert resposta.data["mensagem"] == "25 reservas encontradas."
    assert resposta.data["paginacao"] == {
        "pagina": pagina,
        "tamanho": 20,
        "total": 25,
        "total_de_paginas": 2,
    }


def test_sem_reservas_o_total_de_paginas_e_zero(cliente_gestor):
    # Act
    resposta = _consultar(cliente_gestor, {"pagina": 2})

    # Assert
    assert resposta.status_code == 200
    assert resposta.data == {
        "mensagem": "Nenhuma reserva encontrada.",
        "dados": [],
        "paginacao": {"pagina": 2, "tamanho": 20, "total": 0, "total_de_paginas": 0},
    }


@pytest.mark.parametrize(
    ("parametros", "campo"),
    [
        ({"pagina": "0"}, "pagina"),
        ({"pagina": "-1"}, "pagina"),
        ({"pagina": "abc"}, "pagina"),
        ({"pagina": "1.5"}, "pagina"),
        ({"tamanho": "0"}, "tamanho"),
        ({"tamanho": "101"}, "tamanho"),
        ({"tamanho": "dez"}, "tamanho"),
    ],
    ids=[
        "pagina-zero",
        "pagina-negativa",
        "pagina-texto",
        "pagina-fracionaria",
        "tamanho-zero",
        "tamanho-acima-do-maximo",
        "tamanho-texto",
    ],
)
def test_pagina_ou_tamanho_invalidos_respondem_400_com_o_campo(
    cliente_gestor, massa, parametros, campo
):
    # Act
    resposta = _consultar(cliente_gestor, parametros)

    # Assert
    assert resposta.status_code == 400
    assert resposta.data["erro"]["codigo"] == "DADOS_INVALIDOS"
    assert list(resposta.data["erro"]["campos"]) == [campo]


def test_tamanho_no_maximo_e_aceito(cliente_gestor, massa):
    # Act
    resposta = _consultar(cliente_gestor, {"tamanho": 100})

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["paginacao"]["tamanho"] == 100
    assert _ids_de(resposta) == massa


@pytest.mark.parametrize(
    "parametros",
    [{"pagina": ""}, {"tamanho": ""}],
    ids=["pagina-em-branco", "tamanho-em-branco"],
)
def test_pagina_ou_tamanho_em_branco_valem_o_padrao(cliente_gestor, massa, parametros):
    # Act
    resposta = _consultar(cliente_gestor, parametros)

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["paginacao"]["pagina"] == 1
    assert resposta.data["paginacao"]["tamanho"] == 20


def test_filtros_combinados_com_a_paginacao(cliente_gestor, usuario_solicitante, massa):
    # Act
    resposta = _consultar(
        cliente_gestor,
        {"solicitante": usuario_solicitante.matricula, "tamanho": 4, "pagina": 3},
    )

    # Assert
    do_solicitante = [massa[indice] for indice in range(0, 17, 2)]
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "9 reservas encontradas."
    assert _ids_de(resposta) == do_solicitante[8:]
    assert resposta.data["paginacao"] == {
        "pagina": 3,
        "tamanho": 4,
        "total": 9,
        "total_de_paginas": 3,
    }


def test_solicitante_conta_e_pagina_so_as_proprias(cliente_solicitante, massa):
    # Act
    primeira = _consultar(cliente_solicitante, {"tamanho": 5})
    ultima = _consultar(cliente_solicitante, {"tamanho": 5, "pagina": 2})

    # Assert
    do_solicitante = [massa[indice] for indice in range(0, 17, 2)]
    assert primeira.data["mensagem"] == "9 reservas encontradas."
    assert primeira.data["paginacao"]["total"] == DO_SOLICITANTE
    assert primeira.data["paginacao"]["total_de_paginas"] == 2
    assert _ids_de(primeira) + _ids_de(ultima) == do_solicitante
    assert ultima.data["paginacao"]["total"] == DO_SOLICITANTE
