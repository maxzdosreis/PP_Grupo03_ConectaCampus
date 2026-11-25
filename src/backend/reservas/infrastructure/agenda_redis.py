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
from reservas.infrastructure.redis_comum import cliente as _cliente
from reservas.infrastructure.redis_comum import texto as _texto

logger = logging.getLogger(__name__)

MINUTOS_NO_DIA = 24 * 60
FOLGA_DO_TTL = timedelta(days=1)
TTL_MINIMO = timedelta(hours=1)

CONTAGEM_DO_SCAN = 500
_PREFIXO_DA_PROJECAO = "agenda:espaco:"

_SENTINELA = "_"
_SCORE_DA_SENTINELA = -1

_AVANCAR_VERSAO = """
redis.call("INCR", KEYS[2])
redis.call("EXPIRE", KEYS[2], ARGV[3])
"""

_EXIGIR_PROJECAO = """
if not redis.call("ZSCORE", KEYS[1], ARGV[1]) then
    return 0
end
"""

_TIRAR_A_RESERVA = """
for _, membro in ipairs(redis.call("ZRANGE", KEYS[1], 0, -1)) do
    if string.sub(membro, 1, string.len(ARGV[2])) == ARGV[2] then
        redis.call("ZREM", KEYS[1], membro)
    end
end
"""

_REGISTRAR = (
    _AVANCAR_VERSAO
    + _EXIGIR_PROJECAO
    + _TIRAR_A_RESERVA
    + """
redis.call("ZADD", KEYS[1], ARGV[4], ARGV[5])
redis.call("EXPIRE", KEYS[1], ARGV[3])
return 1
"""
)

_REMOVER = _AVANCAR_VERSAO + _EXIGIR_PROJECAO + _TIRAR_A_RESERVA + "return 1"

_SUBSTITUIR = """
local atual = tonumber(redis.call("GET", KEYS[2]) or "0")
if atual ~= tonumber(ARGV[1]) then
    return 0
end
redis.call("DEL", KEYS[1])
for i = 3, #ARGV, 2 do
    redis.call("ZADD", KEYS[1], ARGV[i], ARGV[i + 1])
end
redis.call("EXPIRE", KEYS[1], ARGV[2])
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
                keys=[chave, _chave_da_versao(espaco_id, intervalo.data)],
                args=[
                    _SENTINELA,
                    _prefixo(reserva_id),
                    self._ttl_em_segundos(intervalo.data),
                    _inicio_em_minutos(intervalo),
                    _membro(reserva_id, intervalo, situacao),
                ],
            )
        except RedisError as erro:
            _indisponivel(erro)

    def remover(self, espaco_id: int, reserva_id: int, data: date) -> None:
        chave = _chave(espaco_id, data)
        try:
            script = _cliente(chave, escrita=True).register_script(_REMOVER)
            script(
                keys=[chave, _chave_da_versao(espaco_id, data)],
                args=[_SENTINELA, _prefixo(reserva_id), self._ttl_em_segundos(data)],
            )
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

    def dias_projetados(self, a_partir_de: date) -> frozenset[tuple[int, date]]:
        padrao = cache.make_key(f"{_PREFIXO_DA_PROJECAO}*")
        prefixo = cache.make_key(_PREFIXO_DA_PROJECAO)
        dias = set()
        try:
            for chave in _cliente(padrao, escrita=False).scan_iter(
                match=padrao, count=CONTAGEM_DO_SCAN
            ):
                dia = _interpretar_chave(_texto(chave), prefixo)
                if dia is not None and dia[1] >= a_partir_de:
                    dias.add(dia)
        except RedisError as erro:
            _indisponivel(erro)
        return frozenset(dias)

    def versao(self, espaco_id: int, data: date) -> int:
        chave = _chave_da_versao(espaco_id, data)
        try:
            valor = _cliente(chave, escrita=False).get(chave)
        except RedisError as erro:
            _indisponivel(erro)
        return int(valor) if valor is not None else 0

    def substituir(
        self,
        espaco_id: int,
        data: date,
        ocupados: Mapping[int, HorarioOcupado],
        *,
        versao: int,
    ) -> bool:
        chave = _chave(espaco_id, data)
        argumentos = [
            versao,
            self._ttl_em_segundos(data),
            _SCORE_DA_SENTINELA,
            _SENTINELA,
        ]
        for reserva_id, ocupado in ocupados.items():
            argumentos.append(_inicio_em_minutos(ocupado.intervalo))
            argumentos.append(_membro(reserva_id, ocupado.intervalo, ocupado.situacao))
        try:
            script = _cliente(chave, escrita=True).register_script(_SUBSTITUIR)
            gravou = script(
                keys=[chave, _chave_da_versao(espaco_id, data)], args=argumentos
            )
        except RedisError as erro:
            _indisponivel(erro)
        return bool(gravou)

    def _ttl_em_segundos(self, data: date) -> int:
        fim_do_dia = datetime.combine(
            data + timedelta(days=1), time(0, 0), tzinfo=FUSO_HORARIO
        )
        restante = fim_do_dia - self._relogio() + FOLGA_DO_TTL
        return int(max(restante, TTL_MINIMO).total_seconds())


def _chave(espaco_id: int, data: date) -> str:
    return cache.make_key(f"{_PREFIXO_DA_PROJECAO}{espaco_id}:{data.isoformat()}")


def _interpretar_chave(chave: str, prefixo: str) -> tuple[int, date] | None:
    try:
        espaco, data = chave.removeprefix(prefixo).split(":")
        return int(espaco), date.fromisoformat(data)
    except ValueError:
        logger.warning("Chave da agenda ignorada, formato inesperado: %s", chave)
        return None


def _chave_da_versao(espaco_id: int, data: date) -> str:
    return cache.make_key(f"agenda:versao:espaco:{espaco_id}:{data.isoformat()}")


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
