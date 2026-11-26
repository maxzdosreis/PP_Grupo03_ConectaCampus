import logging
from datetime import time

import pytest

from compartilhado.domain.erros import AcaoNaoPermitida
from reservas.application.ranking_de_espacos import (
    ConsultarRankingDeEspacos,
    PosicaoDoRanking,
)
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import (
    ATOR_ANA,
    GESTOR,
    ConsultaDeEspacosEmMemoria,
    RankingDeEspacosEmMemoria,
    RepositorioReservasEmMemoria,
    espaco_reservavel,
    exatamente,
    momento_para,
    reserva_solicitada,
)

S = SituacaoReserva


def _reserva(repositorio, espaco_id, hora, situacao=S.CONFIRMADA):
    reserva = reserva_solicitada(
        espaco_id=espaco_id, hora_inicio=time(hora, 0), hora_fim=time(hora + 1, 0)
    )
    if situacao is S.CONCLUIDA:
        reserva.alterar_situacao(S.CONFIRMADA, ator=GESTOR, agora=reserva.criada_em)
    if situacao is not S.SOLICITADA:
        reserva.alterar_situacao(
            situacao,
            motivo="Chuva" if situacao is S.CANCELADA else None,
            ator=GESTOR,
            agora=momento_para(situacao),
        )
    return repositorio.salvar(reserva)


def _montar(ranking, repositorio):
    registros = repositorio.listar_para_ranking(0, 1000)
    assert ranking.substituir(registros, versao=ranking.versao())


@pytest.fixture
def repositorio():
    return RepositorioReservasEmMemoria()


@pytest.fixture
def ranking():
    return RankingDeEspacosEmMemoria()


@pytest.fixture
def espacos():
    return ConsultaDeEspacosEmMemoria(
        [
            espaco_reservavel(1, "Quadra Central"),
            espaco_reservavel(2, "Ginásio A"),
            espaco_reservavel(10, "Campo Norte"),
        ]
    )


def _consultar(repositorio, ranking, espacos):
    return ConsultarRankingDeEspacos(repositorio, ranking, espacos)


def _dois_espacos(repositorio):
    _reserva(repositorio, 2, 8)
    _reserva(repositorio, 2, 10, S.CONCLUIDA)
    _reserva(repositorio, 1, 12)
    _reserva(repositorio, 1, 14, S.SOLICITADA)
    _reserva(repositorio, 1, 16, S.CANCELADA)


def test_solicitante_nao_consulta_o_ranking(repositorio, ranking, espacos):
    with pytest.raises(
        AcaoNaoPermitida, match=exatamente(AcaoNaoPermitida.mensagem_padrao)
    ):
        _consultar(repositorio, ranking, espacos).executar(5, ator=ATOR_ANA)


def test_recusa_do_solicitante_nao_toca_no_repositorio_nem_nos_nomes(
    repositorio, ranking, espacos
):
    with pytest.raises(AcaoNaoPermitida):
        _consultar(repositorio, ranking, espacos).executar(5, ator=ATOR_ANA)

    assert repositorio.chamadas_de_contar_por_espaco == 0
    assert not hasattr(espacos, "ids_com_nome_consultados")


def test_com_o_ranking_montado_le_da_projecao_e_nao_do_repositorio(
    repositorio, ranking, espacos
):
    # Arrange
    _dois_espacos(repositorio)
    _montar(ranking, repositorio)

    # Act
    posicoes = _consultar(repositorio, ranking, espacos).executar(5, ator=GESTOR)

    # Assert
    assert posicoes == (
        PosicaoDoRanking(1, 2, "Ginásio A", 2),
        PosicaoDoRanking(2, 1, "Quadra Central", 1),
    )
    assert repositorio.chamadas_de_contar_por_espaco == 0


def test_sem_o_ranking_montado_cai_para_o_repositorio_com_o_mesmo_resultado(
    repositorio, ranking, espacos
):
    # Arrange
    _dois_espacos(repositorio)
    _montar(ranking, repositorio)
    da_projecao = _consultar(repositorio, ranking, espacos).executar(5, ator=GESTOR)

    # Act
    do_banco = _consultar(repositorio, RankingDeEspacosEmMemoria(), espacos).executar(
        5, ator=GESTOR
    )

    # Assert
    assert do_banco == da_projecao
    assert repositorio.chamadas_de_contar_por_espaco == 1


def test_ranking_indisponivel_cai_para_o_repositorio_e_deixa_um_aviso(
    repositorio, espacos, caplog
):
    # Arrange
    _dois_espacos(repositorio)
    ranking = RankingDeEspacosEmMemoria(indisponivel=True)

    # Act
    with caplog.at_level(logging.WARNING):
        posicoes = _consultar(repositorio, ranking, espacos).executar(5, ator=GESTOR)

    # Assert
    assert [p.espaco_id for p in posicoes] == [2, 1]
    assert "Ranking indisponível" in caplog.text


def test_ler_o_ranking_nao_repovoa_a_projecao(repositorio, ranking, espacos):
    # Arrange
    _dois_espacos(repositorio)

    # Act
    _consultar(repositorio, ranking, espacos).executar(5, ator=GESTOR)

    # Assert
    assert ranking.top(5) is None
    assert ranking.versao() == 0


def test_sem_reservas_que_contam_a_resposta_e_vazia(repositorio, ranking, espacos):
    # Arrange
    _reserva(repositorio, 1, 8, S.SOLICITADA)
    _montar(ranking, repositorio)

    # Act
    posicoes = _consultar(repositorio, ranking, espacos).executar(5, ator=GESTOR)

    # Assert
    assert posicoes == ()


def test_respeita_o_limite_pedido(repositorio, ranking, espacos):
    # Arrange
    _dois_espacos(repositorio)
    _montar(ranking, repositorio)

    # Act
    posicoes = _consultar(repositorio, ranking, espacos).executar(1, ator=GESTOR)

    # Assert
    assert [p.espaco_id for p in posicoes] == [2]


def test_empate_vai_para_o_menor_id_do_espaco_com_ids_de_um_e_dois_digitos(
    repositorio, ranking, espacos
):
    # Arrange
    _reserva(repositorio, 10, 8)
    _reserva(repositorio, 2, 10)
    _montar(ranking, repositorio)

    # Act
    com_projecao = _consultar(repositorio, ranking, espacos).executar(5, ator=GESTOR)
    do_banco = _consultar(repositorio, RankingDeEspacosEmMemoria(), espacos).executar(
        5, ator=GESTOR
    )

    # Assert
    assert [p.espaco_id for p in com_projecao] == [2, 10]
    assert do_banco == com_projecao


def test_espaco_sem_nome_conhecido_recebe_o_nome_de_reserva(
    repositorio, ranking, espacos
):
    # Arrange
    _reserva(repositorio, 77, 8)
    _montar(ranking, repositorio)

    # Act
    [posicao] = _consultar(repositorio, ranking, espacos).executar(5, ator=GESTOR)

    # Assert
    assert posicao == PosicaoDoRanking(1, 77, "Espaço 77", 1)


def test_pede_os_nomes_so_dos_espacos_da_resposta(repositorio, ranking, espacos):
    # Arrange
    _dois_espacos(repositorio)
    _montar(ranking, repositorio)

    # Act
    _consultar(repositorio, ranking, espacos).executar(1, ator=GESTOR)

    # Assert
    assert espacos.ids_com_nome_consultados == [2]
