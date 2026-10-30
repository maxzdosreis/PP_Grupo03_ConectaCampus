from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from reservas.domain.regras_de_agenda import (
    ANTECEDENCIA_MAXIMA_EM_DIAS,
    DURACAO_MAXIMA,
    DURACAO_MINIMA,
    HORARIO_DE_ABERTURA,
    HORARIO_DE_FECHAMENTO,
)

pytestmark = pytest.mark.django_db

URL_REGRAS = reverse("reservas:regras_de_agenda")


def test_regras_de_agenda_sem_login_respondem_200_com_as_constantes_do_dominio():
    # Arrange
    data_limite = timezone.localdate() + timedelta(days=ANTECEDENCIA_MAXIMA_EM_DIAS)

    # Act
    resposta = APIClient().get(URL_REGRAS)

    # Assert
    assert resposta.status_code == 200
    assert resposta.data["mensagem"] == "Regras de agenda."
    assert resposta.data["dados"] == {
        "horario_de_abertura": f"{HORARIO_DE_ABERTURA:%H:%M}",
        "horario_de_fechamento": f"{HORARIO_DE_FECHAMENTO:%H:%M}",
        "duracao_minima_em_minutos": DURACAO_MINIMA // timedelta(minutes=1),
        "duracao_maxima_em_minutos": DURACAO_MAXIMA // timedelta(minutes=1),
        "antecedencia_maxima_em_dias": ANTECEDENCIA_MAXIMA_EM_DIAS,
        "data_limite": data_limite.isoformat(),
    }


def test_regras_de_agenda_tem_os_valores_combinados():
    # Act
    dados = APIClient().get(URL_REGRAS).data["dados"]

    # Assert
    assert dados["horario_de_abertura"] == "07:00"
    assert dados["horario_de_fechamento"] == "22:00"
    assert dados["duracao_minima_em_minutos"] == 30
    assert dados["duracao_maxima_em_minutos"] == 180
    assert dados["antecedencia_maxima_em_dias"] == 30
