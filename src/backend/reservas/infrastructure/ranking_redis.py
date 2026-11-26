import logging
from collections import Counter
from collections.abc import Iterable, Iterator
from itertools import islice
from uuid import uuid4

from django.core.cache import cache
from redis.exceptions import RedisError

from reservas.application.portas import (
    RankingDeEspacos,
    RankingIndisponivel,
    RegistroDoRanking,
    validar_janela,
)
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.redis_comum import cliente, texto

logger = logging.getLogger(__name__)

LOTE_DE_GRAVACAO = 1000
TTL_DAS_TEMPORARIAS = 600

_APLICAR = """
redis.call("INCR", KEYS[1])
if redis.call("EXISTS", KEYS[2]) == 0 then
    return 0
end
if ARGV[3] == "1" then
    if redis.call("HSETNX", KEYS[4], ARGV[1], ARGV[2]) == 1 then
        redis.call("ZINCRBY", KEYS[3], 1, ARGV[2])
    end
else
    local espaco = redis.call("HGET", KEYS[4], ARGV[1])
    if espaco then
        redis.call("HDEL", KEYS[4], ARGV[1])
        local total = tonumber(redis.call("ZINCRBY", KEYS[3], -1, espaco))
        if total <= 0 then
            redis.call("ZREM", KEYS[3], espaco)
        end
    end
end
return 1
"""

_TROCAR = """
local atual = tonumber(redis.call("GET", KEYS[1]) or "0")
local vale = atual == tonumber(ARGV[1])
for i = 0, 1 do
    if vale and ARGV[2 + i] == "1" and redis.call("EXISTS", KEYS[5 + i]) == 0 then
        vale = false
    end
end
for i = 0, 1 do
    local definitiva = KEYS[3 + i]
    local temporaria = KEYS[5 + i]
    if not vale then
        redis.call("DEL", temporaria)
    elseif redis.call("EXISTS", temporaria) == 1 then
        redis.call("RENAME", temporaria, definitiva)
        redis.call("PERSIST", definitiva)
    else
        redis.call("DEL", definitiva)
    end
end
if not vale then
    return 0
end
redis.call("SET", KEYS[2], "1")
return 1
"""


class RankingDeEspacosRedis(RankingDeEspacos):
    def aplicar(
        self, reserva_id: int, espaco_id: int, situacao: SituacaoReserva
    ) -> None:
        chaves = [
            _chave_da_versao(),
            _chave_do_sinal(),
            _chave_do_ranking(),
            _chave_do_livro(),
        ]
        try:
            script = cliente(chaves[0], escrita=True).register_script(_APLICAR)
            script(
                keys=chaves,
                args=[reserva_id, espaco_id, int(situacao.conta_no_ranking)],
            )
        except RedisError as erro:
            _indisponivel(erro)

    def top(self, limite: int) -> tuple[tuple[int, int], ...] | None:
        validar_janela(limite, 0)
        ranking = _chave_do_ranking()
        try:
            canal = cliente(ranking, escrita=False).pipeline()
            canal.exists(_chave_do_sinal())
            canal.zrevrange(ranking, 0, limite - 1, withscores=True)
            montado, melhores = canal.execute()
            if not montado:
                return None
            pares = [(int(texto(membro)), int(total)) for membro, total in melhores]
            if len(pares) == limite:
                pares = self._completar_o_empate_do_corte(ranking, pares)
        except RedisError as erro:
            _indisponivel(erro)
        pares.sort(key=lambda par: (-par[1], par[0]))
        return tuple(pares[:limite])

    def _completar_o_empate_do_corte(
        self, ranking: str, pares: list[tuple[int, int]]
    ) -> list[tuple[int, int]]:
        corte = pares[-1][1]
        leitor = cliente(ranking, escrita=False)
        empatados = leitor.zrangebyscore(ranking, corte, corte)
        acima = [par for par in pares if par[1] != corte]
        return acima + [(int(texto(membro)), corte) for membro in empatados]

    def versao(self) -> int:
        chave = _chave_da_versao()
        try:
            valor = cliente(chave, escrita=False).get(chave)
        except RedisError as erro:
            _indisponivel(erro)
        return int(valor) if valor is not None else 0

    def substituir(
        self, registros: Iterable[RegistroDoRanking], *, versao: int
    ) -> bool:
        sufixo = uuid4().hex
        temporarias = _chaves_temporarias(sufixo)
        try:
            criadas = self._montar_temporarias(registros, *temporarias)
            chaves = [
                _chave_da_versao(),
                _chave_do_sinal(),
                _chave_do_ranking(),
                _chave_do_livro(),
            ]
            script = cliente(chaves[0], escrita=True).register_script(_TROCAR)
            trocou = script(
                keys=[*chaves, *temporarias],
                args=[versao, *(int(chave in criadas) for chave in temporarias)],
            )
        except RedisError as erro:
            _indisponivel(erro)
        finally:
            _apagar(temporarias)
        return bool(trocou)

    def _montar_temporarias(
        self, registros: Iterable[RegistroDoRanking], ranking: str, livro: str
    ) -> set[str]:
        gravador = cliente(ranking, escrita=True)
        totais: Counter[int] = Counter()
        criadas: set[str] = set()
        for lote in _em_lotes(registros):
            contadas = {
                registro.reserva_id: registro.espaco_id
                for registro in lote
                if registro.situacao.conta_no_ranking
            }
            if not contadas:
                continue
            totais.update(contadas.values())
            canal = gravador.pipeline(transaction=False)
            canal.hset(livro, mapping=contadas)
            canal.expire(livro, TTL_DAS_TEMPORARIAS)
            canal.execute()
            criadas.add(livro)
        if totais:
            canal = gravador.pipeline(transaction=False)
            canal.zadd(
                ranking, {str(espaco): total for espaco, total in totais.items()}
            )
            canal.expire(ranking, TTL_DAS_TEMPORARIAS)
            canal.execute()
            criadas.add(ranking)
        return criadas


def _em_lotes(
    registros: Iterable[RegistroDoRanking],
) -> Iterator[list[RegistroDoRanking]]:
    iterador = iter(registros)
    while lote := list(islice(iterador, LOTE_DE_GRAVACAO)):
        yield lote


def _apagar(chaves: list[str]) -> None:
    try:
        cliente(chaves[0], escrita=True).delete(*chaves)
    except RedisError:
        logger.warning("Chaves temporárias do ranking não apagadas; o TTL as remove.")


def _chaves_temporarias(sufixo: str) -> list[str]:
    nomes = ("espacos", "contadas")
    return [cache.make_key(f"ranking:tmp:{sufixo}:{nome}") for nome in nomes]


def _chave_do_ranking() -> str:
    return cache.make_key("ranking:espacos")


def _chave_do_livro() -> str:
    return cache.make_key("ranking:contadas")


def _chave_do_sinal() -> str:
    return cache.make_key("ranking:montado")


def _chave_da_versao() -> str:
    return cache.make_key("ranking:versao")


def _indisponivel(erro: RedisError) -> None:
    logger.exception("Redis indisponível no ranking de espaços")
    raise RankingIndisponivel from erro
