import os

import pytest
from django.core.exceptions import ImproperlyConfigured

from config.settings import _redis_url, _taxa

VARIAVEL = "LIMITE_DE_TESTE"


def test_variavel_ausente_usa_o_padrao(monkeypatch):
    # Arrange
    monkeypatch.delenv(VARIAVEL, raising=False)

    # Act / Assert
    assert _taxa(VARIAVEL, "5/min") == "5/min"


def test_variavel_vazia_usa_o_padrao(monkeypatch):
    # Arrange
    monkeypatch.setenv(VARIAVEL, "   ")

    # Act / Assert
    assert _taxa(VARIAVEL, "5/min") == "5/min"


@pytest.mark.parametrize("valor", ["1/s", "30/min", " 100/hour ", "1000/day"])
def test_taxa_no_formato_do_drf_e_aceita(monkeypatch, valor):
    # Arrange
    monkeypatch.setenv(VARIAVEL, valor)

    # Act / Assert
    assert _taxa(VARIAVEL, "5/min") == valor.strip()


@pytest.mark.parametrize(
    "valor", ["5", "5/minuto", "0/min", "abc/min", "-1/min", "5/m", "5 /min"]
)
def test_taxa_invalida_impede_a_subida_com_mensagem_clara(monkeypatch, valor):
    # Arrange
    monkeypatch.setenv(VARIAVEL, valor)

    # Act / Assert
    with pytest.raises(ImproperlyConfigured) as erro:
        _taxa(VARIAVEL, "5/min")
    assert str(erro.value) == (
        "A variável de ambiente LIMITE_DE_TESTE precisa estar no formato N/período, "
        "com N inteiro positivo e período s, min, hour ou day (ex.: 5/min)."
    )


def test_cache_e_o_redis_do_compose(settings):
    # Assert
    cache = settings.CACHES["default"]
    assert cache["BACKEND"] == "django.core.cache.backends.redis.RedisCache"
    assert cache["LOCATION"] == os.environ["REDIS_URL"]


def test_redis_url_ausente_impede_a_subida(monkeypatch):
    # Arrange
    monkeypatch.delenv("REDIS_URL", raising=False)

    # Act / Assert
    with pytest.raises(ImproperlyConfigured) as erro:
        _redis_url()
    assert str(erro.value) == (
        "A variável de ambiente REDIS_URL não está definida. Ela vem do "
        "docker-compose.yml: suba o backend com docker compose up."
    )


def test_ip_dos_limites_ignora_o_x_forwarded_for(settings):
    # Assert
    assert settings.REST_FRAMEWORK["NUM_PROXIES"] == 0
