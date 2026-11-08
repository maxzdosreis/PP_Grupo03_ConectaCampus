import logging
from collections.abc import Mapping

from django.conf import settings
from django.contrib.auth import get_user_model
from redis.exceptions import RedisError
from rest_framework import serializers
from rest_framework.throttling import SimpleRateThrottle

from compartilhado.api.excecoes import ServicoIndisponivel

logger = logging.getLogger(__name__)


class LimiteDeTentativas(SimpleRateThrottle):
    configuracao: str

    def get_rate(self):
        return getattr(settings, self.configuracao)

    def allow_request(self, request, view):
        try:
            return super().allow_request(request, view)
        except RedisError as erro:
            logger.exception("Redis indisponível no limite de tentativas")
            raise ServicoIndisponivel from erro

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
