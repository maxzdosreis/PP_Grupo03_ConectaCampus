import logging
from collections.abc import Callable, Mapping
from datetime import date, datetime, time, timedelta

from django.core.cache import cache
from django.utils import timezone
from redis.exceptions import RedisError

from reservas.application.ocupacao_do_dia import HorarioOcupado
from reservas.application.portas import AgendaDoDia, AgendaIndisponivel
from reservas.domain.intervalo_de_horario import FUSO_HORARIO, IntervaloDeHorario
from reservas.domain.situacao import SituacaoReserva

logger = logging.getLogger(__name__)

MINUTOS_NO_DIA = 24 * 60
FOLGA_DO_TTL = timedelta(days=1)
TTL_MINIMO = timedelta(hours=1)

_SENTINELA = "_"
_SCORE_DA_SENTINELA = -1

_REGISTRAR = """
if not redis.call("ZSCORE", KEYS[1], ARGV[1]) then
    return 0
end
for _, membro in ipairs(redis.call("ZRANGE", KEYS[1], 0, -1)) do
    if string.sub(membro, 1, string.len(ARGV[2])) == ARGV[2] then
        redis.call("ZREM", KEYS[1], membro)
    end
end
redis.call("ZADD", KEYS[1], ARGV[3], ARGV[4])
redis.call("EXPIRE", KEYS[1], ARGV[5])
return 1
"""

_REMOVER = """
if not redis.call("ZSCORE", KEYS[1], ARGV[1]) then
    return 0
end
for _, membro in ipairs(redis.call("ZRANGE", KEYS[1], 0, -1)) do
    if string.sub(membro, 1, string.len(ARGV[2])) == ARGV[2] then
        redis.call("ZREM", KEYS[1], membro)
    end
end
return 1
"""


class AgendaDoDiaRedis(AgendaDoDia):
    def __init__(self, relogio: Callable[[], datetime] = timezone.now) -> None:
        self._relogio = relogio

    def registrar(
        self,
        espaco_id: int,
        reserva_id: int,
        intervalo: IntervaloDeHorario,
        situacao: SituacaoReserva,
    ) -> None:
        if not situacao.ocupa_horario:
            raise ValueError(f"A situação {situacao.value} não ocupa horário.")
        chave = _chave(espaco_id, intervalo.data)
        try:
            script = _cliente(chave, escrita=True).register_script(_REGISTRAR)
            script(
                keys=[chave],
                args=[
                    _SENTINELA,
                    _prefixo(reserva_id),
                    _inicio_em_minutos(intervalo),
                    _membro(reserva_id, intervalo, situacao),
                    self._ttl_em_segundos(intervalo.data),
                ],
            )
        except RedisError as erro:
            _indisponivel(erro)

    def remover(self, espaco_id: int, reserva_id: int, data: date) -> None:
        chave = _chave(espaco_id, data)
        try:
            script = _cliente(chave, escrita=True).register_script(_REMOVER)
            script(keys=[chave], args=[_SENTINELA, _prefixo(reserva_id)])
        except RedisError as erro:
            _indisponivel(erro)

    def listar(self, espaco_id: int, data: date) -> tuple[HorarioOcupado, ...] | None:
        chave = _chave(espaco_id, data)
        try:
            membros = _cliente(chave, escrita=False).zrange(
                chave, 0, -1, withscores=True
            )
        except RedisError as erro:
            _indisponivel(erro)
        if not membros:
            return None
        return tuple(
            _para_horario(data, membro, score)
            for membro, score in membros
            if _texto(membro) != _SENTINELA
        )

    def substituir(
        self, espaco_id: int, data: date, ocupados: Mapping[int, HorarioOcupado]
    ) -> None:
        chave = _chave(espaco_id, data)
        membros = {_SENTINELA: _SCORE_DA_SENTINELA}
        for reserva_id, ocupado in ocupados.items():
            membro = _membro(reserva_id, ocupado.intervalo, ocupado.situacao)
            membros[membro] = _inicio_em_minutos(ocupado.intervalo)
        try:
            with _cliente(chave, escrita=True).pipeline(transaction=True) as pipeline:
                pipeline.delete(chave)
                pipeline.zadd(chave, membros)
                pipeline.expire(chave, self._ttl_em_segundos(data))
                pipeline.execute()
        except RedisError as erro:
            _indisponivel(erro)

    def _ttl_em_segundos(self, data: date) -> int:
        fim_do_dia = datetime.combine(
            data + timedelta(days=1), time(0, 0), tzinfo=FUSO_HORARIO
        )
        restante = fim_do_dia - self._relogio() + FOLGA_DO_TTL
        return int(max(restante, TTL_MINIMO).total_seconds())


def _chave(espaco_id: int, data: date) -> str:
    return cache.make_key(f"agenda:espaco:{espaco_id}:{data.isoformat()}")


def _cliente(chave: str, *, escrita: bool):
    return cache._cache.get_client(chave, write=escrita)


def _indisponivel(erro: RedisError) -> None:
    logger.exception("Redis indisponível na agenda do dia")
    raise AgendaIndisponivel from erro


def _prefixo(reserva_id: int) -> str:
    return f"{reserva_id}:"


def _em_minutos(hora: time) -> int:
    return hora.hour * 60 + hora.minute


def _inicio_em_minutos(intervalo: IntervaloDeHorario) -> int:
    return _em_minutos(intervalo.hora_inicio)


def _fim_em_minutos(intervalo: IntervaloDeHorario) -> int:
    if intervalo.termina_a_meia_noite():
        return MINUTOS_NO_DIA
    return _em_minutos(intervalo.hora_fim)


def _membro(
    reserva_id: int, intervalo: IntervaloDeHorario, situacao: SituacaoReserva
) -> str:
    return f"{reserva_id}:{_fim_em_minutos(intervalo)}:{situacao.value}"


def _texto(valor: bytes | str) -> str:
    return valor.decode() if isinstance(valor, bytes) else valor


def _hora_de(minutos: int) -> time:
    return time(minutos // 60 % 24, minutos % 60)


def _para_horario(data: date, membro: bytes | str, score: float) -> HorarioOcupado:
    _, fim, situacao = _texto(membro).split(":")
    intervalo = IntervaloDeHorario(
        data=data,
        hora_inicio=_hora_de(int(score)),
        hora_fim=_hora_de(int(fim)),
    )
    return HorarioOcupado(intervalo=intervalo, situacao=SituacaoReserva(situacao))
