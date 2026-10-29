import threading
from datetime import datetime, time, timedelta

import pytest
from django.db import connection
from django.utils import timezone

from reservas.application.casos_de_uso import AlterarSituacaoReserva
from reservas.domain.ator import Ator, PapelDoAtor
from reservas.domain.excecoes import ReservaDesatualizada
from reservas.domain.reserva import Reserva
from reservas.domain.situacao import SituacaoReserva
from reservas.domain.solicitante import Solicitante
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango
from reservas.tests.historico import verificar_historico_coerente

S = SituacaoReserva
ANA = Solicitante(usuario_id=7, nome="Ana Souza", matricula="2026001")
GESTOR = Ator(usuario_id=1, nome="Gestora de Teste", papel=PapelDoAtor.GESTOR)
DONA = Ator(usuario_id=ANA.usuario_id, nome=ANA.nome, papel=PapelDoAtor.SOLICITANTE)
ESPERA_MAXIMA_S = 10


class _RepositorioQueEsperaOutraLeitura(RepositorioReservasDjango):
    def __init__(self, barreira: threading.Barrier) -> None:
        self._barreira = barreira

    def obter_por_id(self, reserva_id: int) -> Reserva | None:
        reserva = super().obter_por_id(reserva_id)
        self._barreira.wait(timeout=ESPERA_MAXIMA_S)
        return reserva


def _alterar_em_paralelo(reserva_id, pedidos):
    barreira = threading.Barrier(len(pedidos))
    resultados = {}

    def alterar(nome, ator, nova, motivo):
        try:
            AlterarSituacaoReserva(
                _RepositorioQueEsperaOutraLeitura(barreira), timezone.now
            ).executar(
                reserva_id=reserva_id, nova_situacao=nova, motivo=motivo, ator=ator
            )
            resultados[nome] = "ok"
        except ReservaDesatualizada as erro:
            resultados[nome] = erro
        finally:
            connection.close()

    threads = [threading.Thread(target=alterar, args=pedido) for pedido in pedidos]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=ESPERA_MAXIMA_S)
    return resultados


@pytest.mark.django_db(transaction=True)
def test_alteracoes_simultaneas_gravam_so_uma_e_o_historico_fica_coerente():
    # Arrange
    repositorio = RepositorioReservasDjango()
    reserva_id = repositorio.salvar(
        Reserva.solicitar(
            espaco_id=1,
            solicitante=ANA,
            data=timezone.localdate() + timedelta(days=1),
            hora_inicio=time(10, 0),
            hora_fim=time(11, 0),
            finalidade="Treino",
            agora=datetime.now(tz=timezone.get_current_timezone()),
        )
    ).id

    # Act
    resultados = _alterar_em_paralelo(
        reserva_id,
        [
            ("gestor", GESTOR, S.CONFIRMADA, None),
            ("dona", DONA, S.CANCELADA, "Não poderei comparecer"),
        ],
    )

    # Assert
    assert set(resultados) == {"gestor", "dona"}, "uma das threads não terminou"
    vencedores = [nome for nome, valor in resultados.items() if valor == "ok"]
    assert len(vencedores) == 1, f"as duas alterações foram gravadas: {resultados}"
    (vencedor,) = vencedores
    (recusa,) = [valor for valor in resultados.values() if valor != "ok"]
    situacao_final = repositorio.obter_por_id(reserva_id).situacao
    assert situacao_final is {"gestor": S.CONFIRMADA, "dona": S.CANCELADA}[vencedor]
    assert isinstance(recusa, ReservaDesatualizada)
    assert recusa.situacao_atual is situacao_final
    historico = repositorio.listar_historico(reserva_id)
    assert len(historico) == 2
    verificar_historico_coerente(historico, situacao_final)
