import logging
from datetime import time

import pytest
from django.core.cache import cache
from redis.exceptions import RedisError

from compartilhado.infrastructure.redis_comum import cliente
from espacos.application.portas import CacheDeEspacosIndisponivel
from espacos.domain.horario_de_funcionamento import HorarioDeFuncionamento
from espacos.domain.tipo_espaco import TipoEspaco
from espacos.infrastructure import cache_de_espacos_redis
from espacos.infrastructure.cache_de_espacos_redis import (
    TTL_DO_ESPACO_EM_SEGUNDOS,
    CacheDeEspacosRedis,
)
from espacos.tests.fakes import CacheDeEspacosEmMemoria, novo_espaco

pytestmark = pytest.mark.django_db

ID = 7


@pytest.fixture(params=["em_memoria", "redis"])
def cache_de_espacos(request):
    if request.param == "em_memoria":
        return CacheDeEspacosEmMemoria()
    return CacheDeEspacosRedis()


@pytest.fixture
def redis_de_espacos():
    return CacheDeEspacosRedis()


def _chave(espaco_id=ID):
    return cache.make_key(f"espaco:{espaco_id}")


def _espaco(**sobrescritas):
    return novo_espaco(id=ID, **sobrescritas)


def _guardar(cache_de_espacos, espaco):
    assert cache_de_espacos.guardar(espaco, versao=cache_de_espacos.versao(espaco.id))


def test_obter_sem_nada_guardado_devolve_none(cache_de_espacos):
    assert cache_de_espacos.obter(ID) is None


def test_guardar_e_obter_devolvem_todos_os_campos(cache_de_espacos):
    # Arrange
    espaco = _espaco(
        nome="Quadra de Areia",
        tipo=TipoEspaco.QUADRA_DE_AREIA,
        capacidade=12,
        ativo=False,
        horario=HorarioDeFuncionamento.padrao().com(
            abertura=time(8, 0), fechamento=time(22, 30)
        ),
    )

    # Act
    _guardar(cache_de_espacos, espaco)
    lido = cache_de_espacos.obter(ID)

    # Assert
    assert lido == espaco
    assert lido.estado == espaco.estado


def test_guardar_com_versao_velha_devolve_false_e_nao_grava(cache_de_espacos):
    # Arrange
    versao_lida = cache_de_espacos.versao(ID)
    cache_de_espacos.invalidar(ID)

    # Act
    gravou = cache_de_espacos.guardar(_espaco(), versao=versao_lida)

    # Assert
    assert gravou is False
    assert cache_de_espacos.obter(ID) is None


def test_invalidar_apaga_o_guardado_e_avanca_a_versao(cache_de_espacos):
    # Arrange
    _guardar(cache_de_espacos, _espaco())
    antes = cache_de_espacos.versao(ID)

    # Act
    cache_de_espacos.invalidar(ID)

    # Assert
    assert cache_de_espacos.obter(ID) is None
    assert cache_de_espacos.versao(ID) == antes + 1


def test_invalidar_sem_nada_guardado_tambem_avanca_a_versao(cache_de_espacos):
    # Act
    cache_de_espacos.invalidar(ID)

    # Assert
    assert cache_de_espacos.versao(ID) == 1


def test_o_hash_tem_ttl_positivo_e_no_maximo_o_teto(redis_de_espacos):
    # Arrange
    _guardar(redis_de_espacos, _espaco())

    # Act
    ttl = cliente(_chave(), escrita=False).ttl(_chave())

    # Assert
    assert 0 < ttl <= TTL_DO_ESPACO_EM_SEGUNDOS


def test_hash_incompleto_vira_miss_e_e_descartado(redis_de_espacos, caplog):
    # Arrange
    cliente(_chave(), escrita=True).hset(_chave(), mapping={"nome": "Só o nome"})

    # Act
    with caplog.at_level(logging.WARNING):
        lido = redis_de_espacos.obter(ID)

    # Assert
    assert lido is None
    assert "quebrada" in caplog.text
    assert cliente(_chave(), escrita=False).exists(_chave()) == 0


@pytest.mark.parametrize(
    ("campo", "valor"),
    [
        ("capacidade", "muitos"),
        ("capacidade", "0"),
        ("tipo", "PISCINA"),
        ("ativo", "talvez"),
        ("fechamento_em_minutos", "1"),
        ("nome", "  "),
    ],
)
def test_valor_que_a_entidade_recusa_vira_miss(redis_de_espacos, campo, valor):
    # Arrange
    campos = {
        "nome": "Ginásio",
        "tipo": "GINASIO",
        "capacidade": "10",
        "ativo": "1",
        "abertura_em_minutos": "420",
        "fechamento_em_minutos": "1440",
        campo: valor,
    }
    cliente(_chave(), escrita=True).hset(_chave(), mapping=campos)

    # Act e Assert
    assert redis_de_espacos.obter(ID) is None


def test_chave_com_tipo_errado_vira_indisponivel_sem_derrubar(redis_de_espacos):
    # Arrange
    cliente(_chave(), escrita=True).set(_chave(), "texto solto")

    # Act e Assert
    with pytest.raises(CacheDeEspacosIndisponivel):
        redis_de_espacos.obter(ID)


def test_script_flush_nao_quebra_guardar_nem_invalidar(redis_de_espacos):
    # Arrange
    cliente(_chave(), escrita=True).script_flush()

    # Act
    _guardar(redis_de_espacos, _espaco())
    redis_de_espacos.invalidar(ID)

    # Assert
    assert redis_de_espacos.obter(ID) is None


def test_descartar_com_redis_fora_so_registra_aviso(
    redis_de_espacos, monkeypatch, caplog
):
    # Arrange
    cliente(_chave(), escrita=True).hset(_chave(), mapping={"nome": "x"})
    original = cache_de_espacos_redis.cliente

    def cliente_que_nao_apaga(chave, *, escrita):
        if escrita:
            raise RedisError("fora do ar")
        return original(chave, escrita=escrita)

    monkeypatch.setattr(cache_de_espacos_redis, "cliente", cliente_que_nao_apaga)

    # Act
    with caplog.at_level(logging.WARNING):
        lido = redis_de_espacos.obter(ID)

    # Assert
    assert lido is None
    assert "Não foi possível descartar" in caplog.text


@pytest.mark.parametrize("operacao", ["obter", "versao", "guardar", "invalidar"])
def test_redis_fora_do_ar_vira_indisponivel(redis_de_espacos, monkeypatch, operacao):
    # Arrange
    def cliente_que_falha(chave, *, escrita):
        raise RedisError("fora do ar")

    monkeypatch.setattr(cache_de_espacos_redis, "cliente", cliente_que_falha)
    chamadas = {
        "obter": lambda: redis_de_espacos.obter(ID),
        "versao": lambda: redis_de_espacos.versao(ID),
        "guardar": lambda: redis_de_espacos.guardar(_espaco(), versao=0),
        "invalidar": lambda: redis_de_espacos.invalidar(ID),
    }

    # Act e Assert
    with pytest.raises(CacheDeEspacosIndisponivel):
        chamadas[operacao]()
