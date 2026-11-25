import threading
from datetime import time, timedelta

import pytest
from django.db import connection
from django.urls import reverse
from django.utils import timezone

from reservas.api import dependencias
from reservas.domain.excecoes import ConflitoDeHorario
from reservas.domain.intervalo_de_horario import IntervaloDeHorario
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.indice_redis import IndiceDeReservasRedis
from reservas.tests.fakes import ANA
from reservas.tests.redis_de_teste import (
    afirmar_indice_igual_ao_postgres,
    ids_da_fila,
    ids_da_situacao,
    membros_da_agenda,
    montar_indice,
    ocupados_do_postgres,
    ocupados_do_redis,
    projetar_dia,
    redis_limpo_depois,  # noqa: F401
)

pytestmark = [
    pytest.mark.django_db(transaction=True),
    pytest.mark.usefixtures("redis_limpo_depois"),
]

ESPERA_MAXIMA_S = 20
S = SituacaoReserva
COM_E_SEM_PROJECAO = pytest.mark.parametrize(
    "com_projecao", [True, False], ids=["com_projecao", "sem_projecao"]
)


def _amanha():
    return timezone.localdate() + timedelta(days=1)


def _novo_espaco(cliente_gestor, numero):
    resposta = cliente_gestor.post(
        reverse("espacos:lista"),
        {"nome": f"Quadra {numero}", "tipo": "QUADRA_POLIESPORTIVA", "capacidade": 10},
        format="json",
    )
    return resposta.data["dados"]["id"]


def _horario(inicio, fim):
    hora_inicio, minuto_inicio = inicio
    hora_fim, minuto_fim = fim
    return time(hora_inicio, minuto_inicio), time(hora_fim, minuto_fim)


def _preparar(espaco_ids, com_projecao):
    if not com_projecao:
        return
    for espaco_id in espaco_ids:
        projetar_dia(espaco_id, _amanha())
    montar_indice()


def _criar_em_paralelo(pedidos):
    """pedidos: (nome, espaco_id, (hora, min) do início, (hora, min) do fim)."""
    barreira = threading.Barrier(len(pedidos))
    resultados = {}

    def criar(nome, espaco_id, inicio, fim):
        hora_inicio, hora_fim = _horario(inicio, fim)
        try:
            barreira.wait(timeout=ESPERA_MAXIMA_S)
            resultados[nome] = dependencias.criar_reserva().executar(
                espaco_id=espaco_id,
                solicitante=ANA,
                data=_amanha(),
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
                finalidade="Treino",
            )
        except Exception as erro:  # noqa: BLE001 - a asserção mostra qual foi
            resultados[nome] = erro
        finally:
            connection.close()

    threads = [
        threading.Thread(target=criar, args=pedido, daemon=True) for pedido in pedidos
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=ESPERA_MAXIMA_S)
    assert set(resultados) == {p[0] for p in pedidos}, "uma das threads não terminou"
    return resultados


def _aceitas(resultados):
    return {n: r for n, r in resultados.items() if not isinstance(r, Exception)}


def _recusadas(resultados):
    return {n: r for n, r in resultados.items() if isinstance(r, Exception)}


def _afirmar_que_o_redis_e_o_postgres(espaco_ids):
    for espaco_id in espaco_ids:
        assert ocupados_do_redis(espaco_id, _amanha()) == ocupados_do_postgres(
            espaco_id, _amanha()
        )
    afirmar_indice_igual_ao_postgres()


def _reconstruir_as_projecoes():
    dependencias.reconstruir_agenda().executar()
    montar_indice()


def _levar_as_projecoes_ao_estado_final(espaco_ids, com_projecao):
    if not com_projecao:
        for espaco_id in espaco_ids:
            assert ocupados_do_redis(espaco_id, _amanha()) is None
        assert IndiceDeReservasRedis().pendentes(1) is None
        _reconstruir_as_projecoes()


@COM_E_SEM_PROJECAO
def test_criacoes_simultaneas_no_mesmo_horario_deixam_so_uma_reserva(
    cliente_gestor, com_projecao
):
    # Arrange
    espaco_id = _novo_espaco(cliente_gestor, 1)
    _preparar([espaco_id], com_projecao)
    pedidos = [(f"p{i}", espaco_id, (10, 0), (11, 0)) for i in range(5)]

    # Act
    resultados = _criar_em_paralelo(pedidos)

    # Assert
    aceitas, recusadas = _aceitas(resultados), _recusadas(resultados)
    assert len(aceitas) == 1, f"mais de uma reserva gravada: {resultados}"
    assert len(recusadas) == 4
    assert all(isinstance(r, ConflitoDeHorario) for r in recusadas.values()), recusadas
    (reserva,) = aceitas.values()
    gravadas = ocupados_do_postgres(espaco_id, _amanha())
    assert [g.situacao for g in gravadas] == [S.SOLICITADA]
    if com_projecao:
        assert membros_da_agenda(espaco_id, _amanha()) == [
            f"{reserva.id}:660:SOLICITADA"
        ]
        assert ids_da_fila() == [reserva.id]
        assert ids_da_situacao(S.SOLICITADA) == {reserva.id}
        assert IndiceDeReservasRedis().contagem_por_situacao()[S.SOLICITADA] == 1
    _levar_as_projecoes_ao_estado_final([espaco_id], com_projecao)
    assert membros_da_agenda(espaco_id, _amanha()) == [f"{reserva.id}:660:SOLICITADA"]
    _afirmar_que_o_redis_e_o_postgres([espaco_id])


@COM_E_SEM_PROJECAO
def test_criacoes_simultaneas_em_espacos_diferentes_nao_geram_falso_conflito(
    cliente_gestor, com_projecao
):
    # Arrange
    espaco_ids = [_novo_espaco(cliente_gestor, numero) for numero in range(1, 6)]
    _preparar(espaco_ids, com_projecao)
    pedidos = [
        (f"e{i}", espaco_id, (10, 0), (11, 0)) for i, espaco_id in enumerate(espaco_ids)
    ]

    # Act
    resultados = _criar_em_paralelo(pedidos)

    # Assert
    assert len(_aceitas(resultados)) == 5, f"houve falso conflito: {resultados}"
    if com_projecao:
        for espaco_id in espaco_ids:
            assert len(membros_da_agenda(espaco_id, _amanha())) == 1
        assert len(ids_da_fila()) == 5
    _levar_as_projecoes_ao_estado_final(espaco_ids, com_projecao)
    for espaco_id in espaco_ids:
        assert len(membros_da_agenda(espaco_id, _amanha())) == 1
    _afirmar_que_o_redis_e_o_postgres(espaco_ids)


@COM_E_SEM_PROJECAO
def test_criacoes_com_sobreposicao_parcial_aceitam_so_horarios_que_nao_se_tocam(
    cliente_gestor, com_projecao
):
    # Arrange
    espaco_id = _novo_espaco(cliente_gestor, 1)
    _preparar([espaco_id], com_projecao)
    horarios = {
        "a": ((10, 0), (11, 0)),
        "b": ((10, 30), (11, 30)),
        "c": ((11, 0), (12, 0)),
        "d": ((11, 30), (12, 30)),
        "e": ((12, 0), (13, 0)),
    }
    pedidos = [(nome, espaco_id, *horario) for nome, horario in horarios.items()]

    # Act
    resultados = _criar_em_paralelo(pedidos)

    # Assert
    def intervalo(nome):
        inicio, fim = _horario(*horarios[nome])
        return IntervaloDeHorario(data=_amanha(), hora_inicio=inicio, hora_fim=fim)

    aceitas, recusadas = _aceitas(resultados), _recusadas(resultados)
    assert all(isinstance(r, ConflitoDeHorario) for r in recusadas.values()), recusadas
    assert aceitas, "nenhuma reserva foi aceita"
    for nome in aceitas:
        for outro in aceitas.keys() - {nome}:
            assert not intervalo(nome).sobrepoe(intervalo(outro)), (nome, outro)
    for nome in recusadas:
        assert any(intervalo(nome).sobrepoe(intervalo(a)) for a in aceitas), nome
    assert len(ocupados_do_postgres(espaco_id, _amanha())) == len(aceitas)
    _levar_as_projecoes_ao_estado_final([espaco_id], com_projecao)
    _afirmar_que_o_redis_e_o_postgres([espaco_id])
