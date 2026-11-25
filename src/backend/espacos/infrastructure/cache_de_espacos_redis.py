import logging

from django.core.cache import cache
from redis.exceptions import RedisError

from compartilhado.domain.erros import ErroDeDominio
from compartilhado.infrastructure.redis_comum import cliente, texto
from espacos.application.portas import CacheDeEspacos, CacheDeEspacosIndisponivel
from espacos.domain.espaco_esportivo import EspacoEsportivo
from espacos.domain.horario_de_funcionamento import HorarioDeFuncionamento

logger = logging.getLogger(__name__)

TTL_DO_ESPACO_EM_SEGUNDOS = 300
TTL_DA_VERSAO_EM_SEGUNDOS = 24 * 60 * 60

_GUARDAR = """
local atual = tonumber(redis.call("GET", KEYS[2]) or "0")
if atual ~= tonumber(ARGV[1]) then
    return 0
end
redis.call("DEL", KEYS[1])
redis.call("HSET", KEYS[1], unpack(ARGV, 3))
redis.call("EXPIRE", KEYS[1], ARGV[2])
return 1
"""

_INVALIDAR = """
redis.call("DEL", KEYS[1])
redis.call("INCR", KEYS[2])
redis.call("EXPIRE", KEYS[2], ARGV[1])
"""


class CacheDeEspacosRedis(CacheDeEspacos):
    def obter(self, espaco_id: int) -> EspacoEsportivo | None:
        chave = _chave(espaco_id)
        try:
            campos = cliente(chave, escrita=False).hgetall(chave)
        except RedisError as erro:
            _indisponivel(erro)
        if not campos:
            return None
        try:
            return _para_entidade(
                espaco_id, {texto(k): texto(v) for k, v in campos.items()}
            )
        except (ErroDeDominio, KeyError, ValueError, TypeError):
            logger.warning(
                "Entrada %s do cache de espaços quebrada; descartada.", chave
            )
            self._descartar(chave)
            return None

    def versao(self, espaco_id: int) -> int:
        chave = _chave_da_versao(espaco_id)
        try:
            valor = cliente(chave, escrita=False).get(chave)
        except RedisError as erro:
            _indisponivel(erro)
        return int(valor) if valor is not None else 0

    def guardar(self, espaco: EspacoEsportivo, *, versao: int) -> bool:
        chave = _chave(espaco.id)
        argumentos = [versao, TTL_DO_ESPACO_EM_SEGUNDOS]
        for campo, valor in _como_campos(espaco).items():
            argumentos += [campo, valor]
        try:
            script = cliente(chave, escrita=True).register_script(_GUARDAR)
            gravou = script(keys=[chave, _chave_da_versao(espaco.id)], args=argumentos)
        except RedisError as erro:
            _indisponivel(erro)
        return bool(gravou)

    def invalidar(self, espaco_id: int) -> None:
        chave = _chave(espaco_id)
        try:
            script = cliente(chave, escrita=True).register_script(_INVALIDAR)
            script(
                keys=[chave, _chave_da_versao(espaco_id)],
                args=[TTL_DA_VERSAO_EM_SEGUNDOS],
            )
        except RedisError as erro:
            _indisponivel(erro)

    def _descartar(self, chave: str) -> None:
        try:
            cliente(chave, escrita=True).delete(chave)
        except RedisError:
            logger.warning("Não foi possível descartar a entrada quebrada %s.", chave)


def _chave(espaco_id: int) -> str:
    return cache.make_key(f"espaco:{espaco_id}")


def _chave_da_versao(espaco_id: int) -> str:
    return cache.make_key(f"espaco:versao:{espaco_id}")


def _indisponivel(erro: RedisError) -> None:
    logger.exception("Redis indisponível no cache de espaços")
    raise CacheDeEspacosIndisponivel from erro


def _como_campos(espaco: EspacoEsportivo) -> dict[str, str | int]:
    return {
        "nome": espaco.nome,
        "tipo": espaco.tipo.value,
        "capacidade": espaco.capacidade,
        "ativo": int(espaco.ativo),
        "abertura_em_minutos": espaco.horario.abertura_em_minutos,
        "fechamento_em_minutos": espaco.horario.fechamento_em_minutos,
    }


def _para_entidade(espaco_id: int, campos: dict[str, str]) -> EspacoEsportivo:
    if campos["ativo"] not in ("0", "1"):
        raise ValueError("ativo")
    return EspacoEsportivo(
        id=espaco_id,
        nome=campos["nome"],
        tipo=campos["tipo"],
        capacidade=int(campos["capacidade"]),
        ativo=campos["ativo"] == "1",
        horario=HorarioDeFuncionamento(
            int(campos["abertura_em_minutos"]), int(campos["fechamento_em_minutos"])
        ),
    )
