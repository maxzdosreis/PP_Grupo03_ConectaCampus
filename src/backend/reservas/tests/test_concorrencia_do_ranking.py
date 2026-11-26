import threading

import pytest
from django.core.cache import cache

from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.ranking_redis import RankingDeEspacosRedis
from reservas.infrastructure.redis_comum import cliente

pytestmark = pytest.mark.django_db

TAREFAS = 20
ESPERA_MAXIMA_S = 10


def _em_paralelo(acoes) -> None:
    barreira = threading.Barrier(len(acoes))
    erros: list[BaseException] = []

    def rodar(acao):
        try:
            barreira.wait(timeout=ESPERA_MAXIMA_S)
            acao()
        except BaseException as erro:  # noqa: BLE001 - o teste repassa tudo
            erros.append(erro)

    threads = [threading.Thread(target=rodar, args=(acao,)) for acao in acoes]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=ESPERA_MAXIMA_S * 2)
    assert not erros


@pytest.fixture
def ranking():
    montado = RankingDeEspacosRedis()
    assert montado.substituir([], versao=montado.versao())
    return montado


def test_vinte_reservas_distintas_no_mesmo_espaco_somam_vinte_sem_perda(ranking):
    # Arrange
    acoes = [
        lambda i=i: RankingDeEspacosRedis().aplicar(i, 7, SituacaoReserva.CONFIRMADA)
        for i in range(1, TAREFAS + 1)
    ]

    # Act
    _em_paralelo(acoes)

    # Assert
    assert ranking.top(5) == ((7, TAREFAS),)
    assert ranking.versao() == TAREFAS


def test_vinte_aplicacoes_da_mesma_reserva_contam_uma_vez(ranking):
    # Arrange
    acoes = [
        lambda: RankingDeEspacosRedis().aplicar(1, 7, SituacaoReserva.CONFIRMADA)
        for _ in range(TAREFAS)
    ]

    # Act
    _em_paralelo(acoes)

    # Assert
    assert ranking.top(5) == ((7, 1),)


def test_confirmar_e_cancelar_a_mesma_reserva_ao_mesmo_tempo_termina_coerente(
    ranking,
):
    # Arrange
    acoes = [
        lambda situacao=situacao: RankingDeEspacosRedis().aplicar(1, 7, situacao)
        for situacao in [SituacaoReserva.CONFIRMADA, SituacaoReserva.CANCELADA]
        * (TAREFAS // 2)
    ]

    # Act
    _em_paralelo(acoes)

    # Assert
    chave_do_livro = cache.make_key("ranking:contadas")
    no_livro = cliente(chave_do_livro, escrita=False).hlen(chave_do_livro)
    assert ranking.top(5) == (((7, 1),) if no_livro else ())
