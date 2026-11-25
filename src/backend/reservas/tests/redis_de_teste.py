import socket
from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from datetime import date

import pytest
from django.core.cache import cache, caches

from reservas.api import dependencias
from reservas.application.ocupacao_do_dia import HorarioOcupado, ocupados_por_reserva
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.agenda_redis import AgendaDoDiaRedis
from reservas.infrastructure.indice_redis import IndiceDeReservasRedis
from reservas.infrastructure.redis_comum import cliente, texto
from reservas.infrastructure.repositorio_django import RepositorioReservasDjango

BANCO_DE_TESTE = 1
_SENTINELA = "_"


def _chave_da_agenda(espaco_id: int, data: date) -> str:
    return cache.make_key(f"agenda:espaco:{espaco_id}:{data.isoformat()}")


def _chave_da_fila() -> str:
    return cache.make_key("reservas:pendentes")


def _chave_da_situacao(situacao: SituacaoReserva) -> str:
    return cache.make_key(f"reservas:situacao:{situacao.value}")


def membros_da_agenda(espaco_id: int, data: date) -> list[str]:
    chave = _chave_da_agenda(espaco_id, data)
    membros = cliente(chave, escrita=False).zrange(chave, 0, -1)
    return sorted(m for m in map(texto, membros) if m != _SENTINELA)


def ids_da_fila() -> list[int]:
    chave = _chave_da_fila()
    return [int(texto(m)) for m in cliente(chave, escrita=False).zrange(chave, 0, -1)]


def ids_da_situacao(situacao: SituacaoReserva) -> set[int]:
    chave = _chave_da_situacao(situacao)
    return {int(texto(m)) for m in cliente(chave, escrita=False).smembers(chave)}


def projetar_dia(espaco_id: int, data: date) -> None:
    agenda = AgendaDoDiaRedis()
    assert agenda.substituir(espaco_id, data, {}, versao=agenda.versao(espaco_id, data))


def montar_indice() -> None:
    dependencias.reconstruir_indice().executar()
    assert IndiceDeReservasRedis().pendentes(1) is not None


def ocupados_do_postgres(espaco_id: int, data: date) -> list[HorarioOcupado]:
    reservas = RepositorioReservasDjango().listar_que_ocupam_horario(espaco_id, data)
    return em_ordem(ocupados_por_reserva(reservas).values())


def ocupados_do_redis(espaco_id: int, data: date) -> list[HorarioOcupado] | None:
    ocupados = AgendaDoDiaRedis().listar(espaco_id, data)
    return None if ocupados is None else em_ordem(ocupados)


def em_ordem(ocupados: Iterable[HorarioOcupado]) -> list[HorarioOcupado]:
    return sorted(
        ocupados,
        key=lambda o: (o.intervalo.hora_inicio, o.intervalo.hora_fim, o.situacao.value),
    )


def afirmar_indice_igual_ao_postgres() -> list[int]:
    registros = RepositorioReservasDjango().listar_para_indice(0, 10_000)
    solicitadas = sorted(
        (r for r in registros if r.situacao is SituacaoReserva.SOLICITADA),
        key=lambda r: (r.criada_em.timestamp(), r.reserva_id),
    )
    fila = [r.reserva_id for r in solicitadas]
    assert ids_da_fila() == fila
    contagem = IndiceDeReservasRedis().contagem_por_situacao()
    for situacao in SituacaoReserva:
        ids = {r.reserva_id for r in registros if r.situacao is situacao}
        assert ids_da_situacao(situacao) == ids, situacao
        assert contagem[situacao] == len(ids), situacao
    return fila


def limpar_banco_de_teste() -> None:
    chave = _chave_da_fila()
    redis = cliente(chave, escrita=True)
    banco = redis.connection_pool.connection_kwargs["db"]
    assert banco == BANCO_DE_TESTE, f"recusado: o banco {banco} não é o de teste"
    redis.flushdb()


@pytest.fixture
def redis_limpo_depois() -> Iterator[None]:
    yield
    limpar_banco_de_teste()


@contextmanager
def redis_em(settings, url: str) -> Iterator[None]:
    anterior = settings.CACHES
    padrao = anterior["default"]
    settings.CACHES = {"default": {**padrao, "LOCATION": url}}
    try:
        yield
    finally:
        caches.close_all()
        settings.CACHES = anterior


@contextmanager
def servidor_que_nao_responde() -> Iterator[str]:
    escuta = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        escuta.bind(("127.0.0.1", 0))
        escuta.listen(16)
        yield f"redis://127.0.0.1:{escuta.getsockname()[1]}/{BANCO_DE_TESTE}"
    finally:
        escuta.close()


def url_de_porta_fechada() -> str:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as livre:
        livre.bind(("127.0.0.1", 0))
        porta = livre.getsockname()[1]
    return f"redis://127.0.0.1:{porta}/{BANCO_DE_TESTE}"
