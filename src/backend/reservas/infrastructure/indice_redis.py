import logging
from collections.abc import Iterable, Iterator
from datetime import datetime
from itertools import islice
from uuid import uuid4

from django.core.cache import cache
from redis.exceptions import RedisError

from reservas.application.portas import (
    IndiceDeReservas,
    IndiceIndisponivel,
    RegistroDoIndice,
    validar_janela,
)
from reservas.domain.situacao import SituacaoReserva
from reservas.infrastructure.redis_comum import cliente, texto

logger = logging.getLogger(__name__)

LOTE_DE_GRAVACAO = 1000
TTL_DAS_TEMPORARIAS = 600
LARGURA_DO_ID = 19

_SITUACOES = tuple(SituacaoReserva)

_APLICAR = """
redis.call("INCR", KEYS[1])
if redis.call("EXISTS", KEYS[2]) == 0 then
    return 0
end
local alvo = tonumber(ARGV[2])
for i = 1, 5 do
    if i == alvo then
        redis.call("SADD", KEYS[3 + i], ARGV[1])
    else
        redis.call("SREM", KEYS[3 + i], ARGV[1])
    end
end
if ARGV[5] == "1" then
    redis.call("ZADD", KEYS[3], ARGV[3], ARGV[4])
else
    redis.call("ZREM", KEYS[3], ARGV[4])
end
return 1
"""

_TROCAR = """
local atual = tonumber(redis.call("GET", KEYS[1]) or "0")
local vale = atual == tonumber(ARGV[1])
for i = 0, 5 do
    local definitiva = KEYS[3 + i]
    local temporaria = KEYS[9 + i]
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


class IndiceDeReservasRedis(IndiceDeReservas):
    def aplicar(
        self, reserva_id: int, situacao: SituacaoReserva, criada_em: datetime
    ) -> None:
        chaves = [_chave_da_versao(), _chave_do_sinal(), _chave_da_fila()]
        chaves += [_chave_da_situacao(item) for item in _SITUACOES]
        try:
            script = cliente(chaves[0], escrita=True).register_script(_APLICAR)
            script(
                keys=chaves,
                args=[
                    reserva_id,
                    _SITUACOES.index(situacao) + 1,
                    _score(criada_em),
                    _membro(reserva_id),
                    int(situacao is SituacaoReserva.SOLICITADA),
                ],
            )
        except RedisError as erro:
            _indisponivel(erro)

    def pendentes(self, limite: int, deslocamento: int = 0) -> tuple[int, ...] | None:
        validar_janela(limite, deslocamento)
        fila = _chave_da_fila()
        try:
            canal = cliente(fila, escrita=False).pipeline()
            canal.exists(_chave_do_sinal())
            canal.zrange(fila, deslocamento, deslocamento + limite - 1)
            montado, membros = canal.execute()
        except RedisError as erro:
            _indisponivel(erro)
        if not montado:
            return None
        return tuple(int(texto(membro)) for membro in membros)

    def contagem_por_situacao(self) -> dict[SituacaoReserva, int] | None:
        try:
            canal = cliente(_chave_do_sinal(), escrita=False).pipeline()
            canal.exists(_chave_do_sinal())
            for situacao in _SITUACOES:
                canal.scard(_chave_da_situacao(situacao))
            montado, *totais = canal.execute()
        except RedisError as erro:
            _indisponivel(erro)
        if not montado:
            return None
        return dict(zip(_SITUACOES, totais, strict=True))

    def versao(self) -> int:
        chave = _chave_da_versao()
        try:
            valor = cliente(chave, escrita=False).get(chave)
        except RedisError as erro:
            _indisponivel(erro)
        return int(valor) if valor is not None else 0

    def substituir(self, registros: Iterable[RegistroDoIndice], *, versao: int) -> bool:
        sufixo = uuid4().hex
        temporarias = _chaves_temporarias(sufixo)
        try:
            self._montar_temporarias(registros, temporarias)
            definitivas = [_chave_da_fila()]
            definitivas += [_chave_da_situacao(item) for item in _SITUACOES]
            chaves = [_chave_da_versao(), _chave_do_sinal(), *definitivas]
            script = cliente(chaves[0], escrita=True).register_script(_TROCAR)
            trocou = script(keys=[*chaves, *temporarias], args=[versao])
        except RedisError as erro:
            _indisponivel(erro)
        finally:
            _apagar(temporarias)
        return bool(trocou)

    def _montar_temporarias(
        self, registros: Iterable[RegistroDoIndice], temporarias: list[str]
    ) -> None:
        fila, *por_situacao = temporarias
        chaves_por_situacao = dict(zip(_SITUACOES, por_situacao, strict=True))
        gravador = cliente(fila, escrita=True)
        for lote in _em_lotes(registros):
            canal = gravador.pipeline(transaction=False)
            tocadas = set()
            for registro in lote:
                destino = chaves_por_situacao[registro.situacao]
                canal.sadd(destino, registro.reserva_id)
                tocadas.add(destino)
                if registro.situacao is SituacaoReserva.SOLICITADA:
                    canal.zadd(
                        fila, {_membro(registro.reserva_id): _score(registro.criada_em)}
                    )
                    tocadas.add(fila)
            for chave in tocadas:
                canal.expire(chave, TTL_DAS_TEMPORARIAS)
            canal.execute()


def _em_lotes(
    registros: Iterable[RegistroDoIndice],
) -> Iterator[list[RegistroDoIndice]]:
    iterador = iter(registros)
    while lote := list(islice(iterador, LOTE_DE_GRAVACAO)):
        yield lote


def _apagar(chaves: list[str]) -> None:
    try:
        cliente(chaves[0], escrita=True).delete(*chaves)
    except RedisError:
        logger.warning("Chaves temporárias do índice não apagadas; o TTL as remove.")


def _chaves_temporarias(sufixo: str) -> list[str]:
    nomes = ["pendentes"] + [f"situacao:{item.value}" for item in _SITUACOES]
    return [cache.make_key(f"reservas:tmp:{sufixo}:{nome}") for nome in nomes]


def _chave_da_fila() -> str:
    return cache.make_key("reservas:pendentes")


def _chave_da_situacao(situacao: SituacaoReserva) -> str:
    return cache.make_key(f"reservas:situacao:{situacao.value}")


def _chave_do_sinal() -> str:
    return cache.make_key("reservas:indice:montado")


def _chave_da_versao() -> str:
    return cache.make_key("reservas:indice:versao")


def _membro(reserva_id: int) -> str:
    return f"{reserva_id:0{LARGURA_DO_ID}d}"


def _score(criada_em: datetime) -> str:
    return repr(criada_em.timestamp())


def _indisponivel(erro: RedisError) -> None:
    logger.exception("Redis indisponível no índice de filas e contagens")
    raise IndiceIndisponivel from erro
