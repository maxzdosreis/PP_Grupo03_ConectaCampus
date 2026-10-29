import threading

import pytest
from django.db import connection

from espacos.application.casos_de_uso import DesativarEspaco, EditarEspaco
from espacos.domain.espaco_esportivo import EspacoEsportivo, EstadoDoEspaco
from espacos.domain.excecoes import EspacoDesatualizado
from espacos.domain.tipo_espaco import TipoEspaco
from espacos.infrastructure.repositorio_django import RepositorioEspacosDjango

ESPERA_MAXIMA_S = 10


class _RepositorioQueEsperaOutraLeitura(RepositorioEspacosDjango):
    def __init__(self, barreira: threading.Barrier) -> None:
        self._barreira = barreira

    def obter_por_id(self, espaco_id: int) -> EspacoEsportivo | None:
        espaco = super().obter_por_id(espaco_id)
        self._barreira.wait(timeout=ESPERA_MAXIMA_S)
        return espaco


def _executar_em_paralelo(pedidos):
    barreira = threading.Barrier(len(pedidos))
    resultados = {}

    def executar(nome, acao):
        try:
            acao(_RepositorioQueEsperaOutraLeitura(barreira))
            resultados[nome] = "ok"
        except EspacoDesatualizado as erro:
            resultados[nome] = erro
        finally:
            connection.close()

    threads = [threading.Thread(target=executar, args=pedido) for pedido in pedidos]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=ESPERA_MAXIMA_S)
    return resultados


def _cadastrar():
    return (
        RepositorioEspacosDjango()
        .salvar(
            EspacoEsportivo(nome="Ginásio A", tipo=TipoEspaco.GINASIO, capacidade=20)
        )
        .id
    )


def _vencedor(resultados):
    assert len(resultados) == 2, "uma das threads não terminou"
    vencedores = [nome for nome, valor in resultados.items() if valor == "ok"]
    assert len(vencedores) == 1, f"as duas alterações foram gravadas: {resultados}"
    (recusa,) = [valor for valor in resultados.values() if valor != "ok"]
    assert isinstance(recusa, EspacoDesatualizado)
    return vencedores[0]


@pytest.mark.django_db(transaction=True)
def test_edicao_e_desativacao_simultaneas_gravam_so_uma():
    # Arrange
    espaco_id = _cadastrar()

    # Act
    resultados = _executar_em_paralelo(
        [
            (
                "edicao",
                lambda repo: EditarEspaco(repo).executar(espaco_id, capacidade=99),
            ),
            ("desativacao", lambda repo: DesativarEspaco(repo).executar(espaco_id)),
        ]
    )

    # Assert
    vencedor = _vencedor(resultados)
    estado_final = RepositorioEspacosDjango().obter_por_id(espaco_id).estado
    esperado = {
        "edicao": EstadoDoEspaco("Ginásio A", TipoEspaco.GINASIO, 99, True),
        "desativacao": EstadoDoEspaco("Ginásio A", TipoEspaco.GINASIO, 20, False),
    }[vencedor]
    assert estado_final == esperado


@pytest.mark.django_db(transaction=True)
def test_duas_desativacoes_simultaneas_aceitam_so_uma():
    # Arrange
    espaco_id = _cadastrar()

    def desativar(repo):
        DesativarEspaco(repo).executar(espaco_id)

    # Act
    resultados = _executar_em_paralelo([("a", desativar), ("b", desativar)])

    # Assert
    _vencedor(resultados)
    assert RepositorioEspacosDjango().obter_por_id(espaco_id).ativo is False
