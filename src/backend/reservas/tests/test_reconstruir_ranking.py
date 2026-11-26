import pytest

from reservas.application.portas import RankingIndisponivel, RegistroDoRanking
from reservas.application.reconstruir_ranking import (
    TAMANHO_DO_LOTE,
    TENTATIVAS_DE_RECONSTRUCAO,
    ReconstruirRanking,
    ResultadoDaReconstrucaoDoRanking,
)
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import (
    RankingDeEspacosEmMemoria,
    RepositorioReservasEmMemoria,
)

S = SituacaoReserva


class RepositorioQueConta(RepositorioReservasEmMemoria):
    def __init__(self, registros: list[RegistroDoRanking], ao_ler=lambda: None) -> None:
        super().__init__()
        self._registros = registros
        self._ao_ler = ao_ler
        self.limites: list[int] = []

    def listar_para_ranking(self, depois_de_id, limite):
        self._ao_ler()
        self.limites.append(limite)
        return [r for r in self._registros if r.reserva_id > depois_de_id][:limite]


def _registros(quantidade: int, situacao=S.CONFIRMADA, espaco_id=1):
    return [RegistroDoRanking(i, espaco_id, situacao) for i in range(1, quantidade + 1)]


def test_reconstroi_o_ranking_do_banco_e_conta_espacos_e_reservas_contadas():
    # Arrange
    registros = [
        RegistroDoRanking(1, 7, S.CONFIRMADA),
        RegistroDoRanking(2, 7, S.CONCLUIDA),
        RegistroDoRanking(3, 8, S.CONFIRMADA),
        RegistroDoRanking(4, 8, S.SOLICITADA),
        RegistroDoRanking(5, 9, S.CANCELADA),
        RegistroDoRanking(6, 9, S.RECUSADA),
    ]
    ranking = RankingDeEspacosEmMemoria()

    # Act
    resultado = ReconstruirRanking(RepositorioQueConta(registros), ranking).executar()

    # Assert
    assert resultado == ResultadoDaReconstrucaoDoRanking(2, 3, False)
    assert ranking.top(10) == ((7, 2), (8, 1))


def test_banco_vazio_deixa_o_ranking_montado_e_vazio():
    # Arrange
    ranking = RankingDeEspacosEmMemoria()

    # Act
    resultado = ReconstruirRanking(RepositorioQueConta([]), ranking).executar()

    # Assert
    assert resultado == ResultadoDaReconstrucaoDoRanking(0, 0, False)
    assert ranking.top(10) == ()


def test_le_o_banco_em_lotes_sem_trazer_tudo_de_uma_vez():
    # Arrange
    total = TAMANHO_DO_LOTE * 2 + 1
    repositorio = RepositorioQueConta(_registros(total))
    ranking = RankingDeEspacosEmMemoria()

    # Act
    resultado = ReconstruirRanking(repositorio, ranking).executar()

    # Assert
    assert resultado.reservas_contadas == total
    assert repositorio.limites == [TAMANHO_DO_LOTE] * 4
    assert ranking.top(1) == ((1, total),)


def test_reconstruir_de_novo_da_o_mesmo_resultado():
    # Arrange
    repositorio = RepositorioQueConta(_registros(4))
    ranking = RankingDeEspacosEmMemoria()
    caso_de_uso = ReconstruirRanking(repositorio, ranking)

    # Act
    primeira = caso_de_uso.executar()
    segunda = caso_de_uso.executar()

    # Assert
    assert primeira == segunda
    assert ranking.top(5) == ((1, 4),)


def test_refaz_a_leitura_quando_uma_aplicacao_chega_no_meio():
    # Arrange
    ranking = RankingDeEspacosEmMemoria()
    chegadas = []

    def aplicar_no_meio():
        if not chegadas:
            chegadas.append(1)
            ranking.aplicar(99, 1, S.CONFIRMADA)

    repositorio = RepositorioQueConta(_registros(2), ao_ler=aplicar_no_meio)

    # Act
    resultado = ReconstruirRanking(repositorio, ranking).executar()

    # Assert
    assert resultado.descartado is False
    assert resultado.reservas_contadas == 2


def test_descarta_sem_excecao_depois_das_tentativas_quando_a_versao_nao_para():
    # Arrange
    ranking = RankingDeEspacosEmMemoria()
    contador = iter(range(1000))

    def aplicar_sempre():
        ranking.aplicar(next(contador), 1, S.CONFIRMADA)

    repositorio = RepositorioQueConta(_registros(2), ao_ler=aplicar_sempre)

    # Act
    resultado = ReconstruirRanking(repositorio, ranking).executar()

    # Assert
    assert resultado == ResultadoDaReconstrucaoDoRanking(0, 0, True)
    assert len(repositorio.limites) == TENTATIVAS_DE_RECONSTRUCAO * 2


def test_ranking_indisponivel_sobe_para_quem_chamou():
    # Arrange
    ranking = RankingDeEspacosEmMemoria(indisponivel=True)

    # Act e Assert
    with pytest.raises(RankingIndisponivel):
        ReconstruirRanking(RepositorioQueConta(_registros(1)), ranking).executar()
