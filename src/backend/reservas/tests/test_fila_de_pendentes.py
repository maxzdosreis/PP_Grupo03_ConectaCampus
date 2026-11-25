import logging
from datetime import time, timedelta

import pytest

from compartilhado.domain.erros import AcaoNaoPermitida
from reservas.application.fila_de_pendentes import (
    ConsultarFilaDePendentes,
    ContarReservasPorSituacao,
)
from reservas.application.repositorio import Paginacao
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import (
    AGORA,
    ATOR_ANA,
    GESTOR,
    IndiceDeReservasEmMemoria,
    RepositorioReservasEmMemoria,
    exatamente,
    reserva_solicitada,
)

S = SituacaoReserva


def _solicitar(repositorio, minutos, hora, **sobrescritas):
    return repositorio.salvar(
        reserva_solicitada(
            agora=AGORA + timedelta(minutes=minutos),
            hora_inicio=time(hora, 0),
            hora_fim=time(hora + 1, 0),
            **sobrescritas,
        )
    )


def _montar(indice, repositorio):
    registros = repositorio.listar_para_indice(0, 1000)
    assert indice.substituir(registros, versao=indice.versao())


def _confirmar(repositorio, reserva):
    reserva.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=AGORA)
    repositorio.salvar(reserva)


def _ids(pagina):
    return [reserva.id for reserva in pagina.itens]


@pytest.fixture
def repositorio():
    return RepositorioReservasEmMemoria()


@pytest.fixture
def indice():
    return IndiceDeReservasEmMemoria()


def _fila(repositorio, indice):
    return ConsultarFilaDePendentes(repositorio, indice)


def _contagem(repositorio, indice):
    return ContarReservasPorSituacao(repositorio, indice)


def test_solicitante_nao_consulta_a_fila(repositorio, indice):
    with pytest.raises(
        AcaoNaoPermitida, match=exatamente(AcaoNaoPermitida.mensagem_padrao)
    ):
        _fila(repositorio, indice).executar(Paginacao(), ator=ATOR_ANA)


def test_solicitante_nao_consulta_a_contagem(repositorio, indice):
    with pytest.raises(AcaoNaoPermitida):
        _contagem(repositorio, indice).executar(ator=ATOR_ANA)


def test_recusa_do_solicitante_nao_toca_no_repositorio_nem_no_indice(
    repositorio, indice
):
    with pytest.raises(AcaoNaoPermitida):
        _fila(repositorio, indice).executar(Paginacao(), ator=ATOR_ANA)

    assert repositorio.chamadas_de_listar_pendentes == 0
    assert repositorio.chamadas_de_listar_por_ids == 0


def test_fila_com_indice_montado_nao_usa_a_listagem_do_repositorio(repositorio, indice):
    # Arrange
    primeira = _solicitar(repositorio, 0, 8)
    segunda = _solicitar(repositorio, 5, 10)
    _montar(indice, repositorio)

    # Act
    pagina = _fila(repositorio, indice).executar(Paginacao(), ator=GESTOR)

    # Assert
    assert _ids(pagina) == [primeira.id, segunda.id]
    assert pagina.total == 2
    assert repositorio.chamadas_de_listar_pendentes == 0
    assert repositorio.chamadas_de_listar_por_ids == 1


def test_fila_preserva_a_ordem_de_solicitacao_com_ids_de_um_e_dois_digitos(
    repositorio, indice
):
    # Arrange
    salvas = [_solicitar(repositorio, 0, 8, espaco_id=10 + i) for i in range(12)]
    tardia = _solicitar(repositorio, -30, 8, espaco_id=99)
    _montar(indice, repositorio)

    # Act
    pagina = _fila(repositorio, indice).executar(Paginacao(tamanho=100), ator=GESTOR)

    # Assert
    assert _ids(pagina) == [tardia.id, *[r.id for r in salvas]]
    assert max(_ids(pagina)) >= 10


def test_fila_pagina_e_depois_da_ultima_vem_vazia_com_o_total_certo(
    repositorio, indice
):
    # Arrange
    salvas = [_solicitar(repositorio, i, 8 + i) for i in range(3)]
    _montar(indice, repositorio)
    consulta = _fila(repositorio, indice)

    # Act
    segunda = consulta.executar(Paginacao(numero=2, tamanho=2), ator=GESTOR)
    alem = consulta.executar(Paginacao(numero=3, tamanho=2), ator=GESTOR)

    # Assert
    assert _ids(segunda) == [salvas[2].id]
    assert alem.itens == ()
    assert alem.total == segunda.total == 3


def test_reserva_que_ja_nao_e_solicitada_no_banco_some_da_pagina(repositorio, indice):
    # Arrange
    atrasada = _solicitar(repositorio, 0, 8)
    pendente = _solicitar(repositorio, 5, 10)
    _montar(indice, repositorio)
    _confirmar(repositorio, atrasada)

    # Act
    pagina = _fila(repositorio, indice).executar(Paginacao(), ator=GESTOR)

    # Assert
    assert _ids(pagina) == [pendente.id]
    assert pagina.total == 1
    assert repositorio.chamadas_de_listar_pendentes == 1


def test_id_do_indice_que_nao_existe_no_banco_cai_para_o_repositorio(
    repositorio, indice, caplog
):
    # Arrange
    _solicitar(repositorio, 0, 8)
    _montar(indice, repositorio)
    indice.aplicar(404, S.SOLICITADA, AGORA - timedelta(days=1))

    # Act
    with caplog.at_level(logging.WARNING):
        pagina = _fila(repositorio, indice).executar(Paginacao(), ator=GESTOR)

    # Assert
    assert len(pagina.itens) == 1
    assert pagina.total == 1
    assert "Índice desatualizado" in caplog.text


def test_pagina_cheia_com_id_velho_traz_as_proximas_pendentes_e_o_total_certo(
    repositorio, indice
):
    # Arrange
    primeira, segunda, terceira = (_solicitar(repositorio, i, 8 + i) for i in range(3))
    _montar(indice, repositorio)
    _confirmar(repositorio, primeira)

    # Act
    pagina = _fila(repositorio, indice).executar(Paginacao(tamanho=2), ator=GESTOR)

    # Assert
    assert _ids(pagina) == [segunda.id, terceira.id]
    assert pagina.total == 2


def test_fila_sem_indice_montado_cai_para_o_repositorio(repositorio, indice):
    # Arrange
    primeira = _solicitar(repositorio, 0, 8)
    segunda = _solicitar(repositorio, 5, 10)

    # Act
    pagina = _fila(repositorio, indice).executar(Paginacao(), ator=GESTOR)

    # Assert
    assert _ids(pagina) == [primeira.id, segunda.id]
    assert repositorio.chamadas_de_listar_pendentes == 1
    assert repositorio.chamadas_de_listar_por_ids == 0


def test_fila_com_indice_indisponivel_cai_para_o_repositorio_sem_erro(
    repositorio, indice, caplog
):
    # Arrange
    _solicitar(repositorio, 0, 8)
    indice.indisponivel = True

    # Act
    with caplog.at_level(logging.WARNING):
        pagina = _fila(repositorio, indice).executar(Paginacao(), ator=GESTOR)

    # Assert
    assert pagina.total == 1
    assert "Índice indisponível" in caplog.text


@pytest.mark.parametrize(
    "situacao_do_indice", ["montado", "sem_indice", "indisponivel"]
)
def test_fila_e_igual_com_o_indice_montado_sem_indice_ou_indisponivel(
    repositorio, indice, situacao_do_indice
):
    # Arrange
    for i in range(5):
        _solicitar(repositorio, 10 - i, 8 + i)
    esperado = _fila(repositorio, IndiceDeReservasEmMemoria()).executar(
        Paginacao(numero=2, tamanho=2), ator=GESTOR
    )
    if situacao_do_indice == "montado":
        _montar(indice, repositorio)
    indice.indisponivel = situacao_do_indice == "indisponivel"

    # Act
    pagina = _fila(repositorio, indice).executar(
        Paginacao(numero=2, tamanho=2), ator=GESTOR
    )

    # Assert
    assert pagina == esperado


def test_fila_vazia_com_o_indice_montado(repositorio, indice):
    _montar(indice, repositorio)

    pagina = _fila(repositorio, indice).executar(Paginacao(), ator=GESTOR)

    assert pagina.itens == ()
    assert pagina.total == 0


def test_contagem_com_indice_montado_nao_toca_no_repositorio(repositorio, indice):
    # Arrange
    _solicitar(repositorio, 0, 8)
    confirmada = _solicitar(repositorio, 1, 10)
    _confirmar(repositorio, confirmada)
    _montar(indice, repositorio)

    # Act
    contagem = _contagem(repositorio, indice).executar(ator=GESTOR)

    # Assert
    assert contagem[S.SOLICITADA] == 1
    assert contagem[S.CONFIRMADA] == 1
    assert repositorio.chamadas_de_contar_por_situacao == 0


def test_contagem_traz_as_cinco_situacoes_com_zero(repositorio, indice):
    _montar(indice, repositorio)

    contagem = _contagem(repositorio, indice).executar(ator=GESTOR)

    assert list(contagem) == list(SituacaoReserva)
    assert set(contagem.values()) == {0}


@pytest.mark.parametrize("situacao_do_indice", ["sem_indice", "indisponivel"])
def test_contagem_sem_indice_ou_com_indice_indisponivel_cai_para_o_repositorio(
    repositorio, indice, situacao_do_indice
):
    # Arrange
    _solicitar(repositorio, 0, 8)
    _solicitar(repositorio, 1, 10)
    indice.indisponivel = situacao_do_indice == "indisponivel"

    # Act
    contagem = _contagem(repositorio, indice).executar(ator=GESTOR)

    # Assert
    assert contagem == repositorio.contar_por_situacao()
    assert contagem[S.SOLICITADA] == 2
    assert list(contagem) == list(SituacaoReserva)


def test_contagem_com_indice_indisponivel_registra_aviso(repositorio, indice, caplog):
    indice.indisponivel = True

    with caplog.at_level(logging.WARNING):
        _contagem(repositorio, indice).executar(ator=GESTOR)

    assert "Índice indisponível" in caplog.text
