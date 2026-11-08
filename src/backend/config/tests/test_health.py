import pytest
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

REDIS_FORA_DO_AR = "redis://127.0.0.1:1/0"


def test_health_confere_o_banco_e_o_cache():
    # Act
    resposta = APIClient().get(reverse("health"))

    # Assert
    assert resposta.status_code == 200
    assert resposta.data == {
        "mensagem": "API no ar.",
        "dados": {"banco": "ok", "cache": "ok"},
    }


def test_health_com_o_redis_fora_do_ar_responde_503(settings):
    # Arrange
    settings.CACHES = {
        "default": {**settings.CACHES["default"], "LOCATION": REDIS_FORA_DO_AR}
    }

    # Act
    resposta = APIClient().get(reverse("health"))

    # Assert
    assert resposta.status_code == 503
    assert resposta.data == {
        "erro": {
            "codigo": "CACHE_INDISPONIVEL",
            "mensagem": "Não foi possível conectar ao cache.",
        }
    }
