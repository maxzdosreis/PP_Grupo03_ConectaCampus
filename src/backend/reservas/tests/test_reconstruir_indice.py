from datetime import timedelta

import pytest

from reservas.application.portas import IndiceIndisponivel, RegistroDoIndice
from reservas.application.reconstruir_indice import (
    TAMANHO_DO_LOTE,
    TENTATIVAS_DE_RECONSTRUCAO,
    ReconstruirIndice,
    ResultadoDaReconstrucaoDoIndice,
)
from reservas.domain.situacao import SituacaoReserva
from reservas.tests.fakes import (
    AGORA,
    IndiceDeReservasEmMemoria,
    RepositorioReservasEmMemoria,
)

S = SituacaoReserva


class RepositorioQueConta(RepositorioReservasEmMemoria):
    def __init__(self, registros: list[RegistroDoIndice], ao_ler=lambda: None) -> None:
        super().__init__()
        self._registros = registros
        self._ao_ler = ao_ler
        self.limites: list[int] = []

    def listar_para_indice(self, depois_de_id, limite):
        self._ao_ler()
        self.limites.append(limite)
        return [r for r in self._registros if r.reserva_id > depois_de_id][:limite]


def _registros(quantidade: int, situacao=S.SOLICITADA) -> list[RegistroDoIndice]:
    return [
        RegistroDoIndice(i, situacao, AGORA + timedelta(minutes=i))
        for i in range(1, quantidade + 1)
    ]


def test_reconstroi_o_indice_do_banco_e_conta_reservas_e_pendentes():
    # Arrange
    registros = _registros(3) + [
        RegistroDoIndice(4, S.CONFIRMADA, AGORA),
        RegistroDoIndice(5, S.CONCLUIDA, AGORA),
    ]
    indice = IndiceDeReservasEmMemoria()

    # Act
    resultado = ReconstruirIndice(RepositorioQueConta(registros), indice).executar()

    # Assert
    assert resultado == ResultadoDaReconstrucaoDoIndice(5, 3, False)
    assert indice.pendentes(10) == (1, 2, 3)
    assert indice.contagem_por_situacao()[S.CONFIRMADA] == 1


def test_le_o_banco_em_lotes_sem_trazer_tudo_de_uma_vez():
    # Arrange
    total = TAMANHO_DO_LOTE * 2 + 1
    repositorio = RepositorioQueConta(_registros(total))
    indice = IndiceDeReservasEmMemoria()

    # Act
    resultado = ReconstruirIndice(repositorio, indice).executar()

    # Assert
    assert resultado.reservas_indexadas == total
    assert repositorio.limites == [TAMANHO_DO_LOTE] * 4
    assert len(indice.pendentes(total)) == total


def test_banco_vazio_deixa_o_indice_montado_e_vazio():
    # Arrange
    indice = IndiceDeReservasEmMemoria()

    # Act
    resultado = ReconstruirIndice(RepositorioQueConta([]), indice).executar()

    # Assert
    assert resultado == ResultadoDaReconstrucaoDoIndice(0, 0, False)
    assert indice.pendentes(10) == ()


def test_tenta_de_novo_quando_a_versao_avanca_no_meio():
    # Arrange
    indice = IndiceDeReservasEmMemoria()
    surpresas = []

    def mexer_na_primeira_leitura():
        if not surpresas:
            surpresas.append(True)
            indice.aplicar(99, S.SOLICITADA, AGORA)

    repositorio = RepositorioQueConta(_registros(3), mexer_na_primeira_leitura)

    # Act
    resultado = ReconstruirIndice(repositorio, indice).executar()

    # Assert
    assert resultado == ResultadoDaReconstrucaoDoIndice(3, 3, False)
    assert indice.pendentes(10) == (1, 2, 3)


def test_descarta_sem_erro_depois_de_esgotar_as_tentativas():
    # Arrange
    indice = IndiceDeReservasEmMemoria()
    repositorio = RepositorioQueConta(
        _registros(2), lambda: indice.aplicar(99, S.SOLICITADA, AGORA)
    )

    # Act
    resultado = ReconstruirIndice(repositorio, indice).executar()

    # Assert
    assert resultado == ResultadoDaReconstrucaoDoIndice(0, 0, True)
    assert indice.pendentes(10) is None
    assert indice.versao() == TENTATIVAS_DE_RECONSTRUCAO * 2


def test_indice_indisponivel_sobe():
    # Arrange
    indice = IndiceDeReservasEmMemoria(indisponivel=True)

    # Act e Assert
    with pytest.raises(IndiceIndisponivel):
        ReconstruirIndice(RepositorioQueConta(_registros(1)), indice).executar()
