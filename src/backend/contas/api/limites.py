import logging
from collections.abc import Mapping
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from redis.exceptions import RedisError
from rest_framework import serializers
from rest_framework.throttling import SimpleRateThrottle

from compartilhado.api.excecoes import ServicoIndisponivel

logger = logging.getLogger(__name__)

_REGISTRAR_TENTATIVA = """
local agora = tonumber(ARGV[1])
local janela = tonumber(ARGV[2])
local limite = tonumber(ARGV[3])
redis.call("ZREMRANGEBYSCORE", KEYS[1], "-inf", agora - janela)
local total = redis.call("ZCARD", KEYS[1])
if total >= limite then
    local posicao = total - limite
    local libera = redis.call("ZRANGE", KEYS[1], posicao, posicao, "WITHSCORES")
    return {0, tostring(tonumber(libera[2]) + janela - agora)}
end
redis.call("ZADD", KEYS[1], agora, ARGV[4])
redis.call("EXPIRE", KEYS[1], math.ceil(janela))
return {1, "0"}
"""


class LimiteDeTentativas(SimpleRateThrottle):
    configuracao: str

    def get_rate(self):
        return getattr(settings, self.configuracao)

    def allow_request(self, request, view):
        self._espera = None
        chave = self.get_cache_key(request, view)
        if chave is None:
            return True
        try:
            permitida, self._espera = _registrar_tentativa(
                chave,
                agora=self.timer(),
                janela=self.duration,
                limite=self.num_requests,
            )
        except RedisError as erro:
            logger.exception("Redis indisponível no limite de tentativas")
            raise ServicoIndisponivel from erro
        return permitida

    def wait(self):
        return self._espera

    def _chave(self, identificador):
        return self.cache_format % {"scope": self.scope, "ident": identificador}


class _LimitePorIp(LimiteDeTentativas):
    def get_cache_key(self, request, view):
        return self._chave(self.get_ident(request))


class LimiteDeLoginPorIp(_LimitePorIp):
    scope = "login_ip"
    configuracao = "LIMITE_LOGIN_POR_IP"


class LimiteDeCadastroPorIp(_LimitePorIp):
    scope = "cadastro_ip"
    configuracao = "LIMITE_CADASTRO_POR_IP"


class LimiteDeLoginPorEmail(LimiteDeTentativas):
    scope = "login_email"
    configuracao = "LIMITE_LOGIN_POR_EMAIL"

    def get_cache_key(self, request, view):
        email = _email_utilizavel(request.data)
        return None if email is None else self._chave(email)


def _email_utilizavel(dados):
    valor = dados.get("email") if isinstance(dados, Mapping) else None
    if not isinstance(valor, str):
        return None
    try:
        email = serializers.EmailField().run_validation(valor)
    except serializers.ValidationError:
        return None
    return get_user_model().objects.normalize_email(email)


def _registrar_tentativa(chave, *, agora, janela, limite):
    nome = cache.make_key(chave)
    cliente = cache._cache.get_client(nome, write=True)
    registrar = cliente.register_script(_REGISTRAR_TENTATIVA)
    permitida, espera = registrar(
        keys=[nome], args=[agora, janela, limite, f"{agora}:{uuid4().hex}"]
    )
    return bool(permitida), None if permitida else float(espera)
