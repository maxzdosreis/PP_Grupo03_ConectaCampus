import pytest
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db

ORIGEM_DO_FRONTEND = "http://localhost:5173"


def _health_vindo_de(origem):
    return APIClient().get(reverse("health"), HTTP_ORIGIN=origem)


@override_settings(CORS_ALLOWED_ORIGINS=[ORIGEM_DO_FRONTEND])
def test_origem_configurada_recebe_access_control_allow_origin():
    # Act
    resposta = _health_vindo_de(ORIGEM_DO_FRONTEND)

    # Assert
    assert resposta["Access-Control-Allow-Origin"] == ORIGEM_DO_FRONTEND


@override_settings(CORS_ALLOWED_ORIGINS=[ORIGEM_DO_FRONTEND])
def test_origem_desconhecida_nao_recebe_access_control_allow_origin():
    # Act
    resposta = _health_vindo_de("http://site-malicioso.com")

    # Assert
    assert "Access-Control-Allow-Origin" not in resposta
