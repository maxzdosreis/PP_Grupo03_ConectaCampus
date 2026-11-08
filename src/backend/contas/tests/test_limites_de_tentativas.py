import threading
from types import SimpleNamespace

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from contas.api.limites import (
    LimiteDeLoginPorEmail,
    LimiteDeLoginPorIp,
    LimiteDeTentativas,
)
from contas.infrastructure.models import Usuario

pytestmark = pytest.mark.django_db

URL_LOGIN = reverse("contas:login")
URL_CADASTRO = reverse("contas:cadastro")
URL_REFRESH = reverse("contas:refresh")
EMAIL = "ana@x.com"
OUTRO_EMAIL = "bruno@x.com"
SENHA = "senha-de-teste-123"
LIMITE_POR_EMAIL = 5
LIMITE_POR_IP = 20
LIMITE_DE_CADASTRO = 10
MENSAGEM_DE_UM_MINUTO = "Muitas tentativas. Tente de novo em 60 segundos."
REDIS_FORA_DO_AR = "redis://127.0.0.1:1/0"
SERVICO_INDISPONIVEL = {
    "erro": {
        "codigo": "SERVICO_INDISPONIVEL",
        "mensagem": "Serviço temporariamente indisponível. "
        "Tente de novo em alguns instantes.",
    }
}


class _Relogio:
    def __init__(self):
        self.agora = 1_000_000.0

    def avancar(self, segundos):
        self.agora += segundos


@pytest.fixture(autouse=True)
def _hash_de_senha_rapido(settings):
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]


@pytest.fixture(autouse=True)
def relogio(monkeypatch):
    relogio = _Relogio()
    monkeypatch.setattr(
        LimiteDeTentativas, "timer", staticmethod(lambda: relogio.agora)
    )
    return relogio


@pytest.fixture
def usuario():
    return Usuario.objects.create_user(
        EMAIL, SENHA, nome="Ana Souza", matricula="2026001"
    )


def _login(email=EMAIL, senha="senha-errada", **cabecalhos):
    return APIClient().post(
        URL_LOGIN, {"email": email, "senha": senha}, format="json", **cabecalhos
    )


def _esgotar_por_email(email=EMAIL):
    for _ in range(LIMITE_POR_EMAIL):
        assert _login(email).status_code == 401


def _assert_limite(resposta, mensagem=MENSAGEM_DE_UM_MINUTO):
    assert resposta.status_code == 429
    assert resposta.data == {
        "erro": {"codigo": "LIMITE_DE_TENTATIVAS", "mensagem": mensagem}
    }
    assert resposta["Retry-After"] == "60"


def test_sexta_tentativa_com_o_mesmo_email_responde_429_com_a_espera(usuario):
    # Arrange
    _esgotar_por_email()

    # Act
    resposta = _login()

    # Assert
    _assert_limite(resposta)


def test_senha_certa_tambem_e_recusada_depois_do_limite(usuario):
    # Arrange
    _esgotar_por_email()

    # Act
    resposta = _login(senha=SENHA)

    # Assert
    _assert_limite(resposta)
    usuario.refresh_from_db()
    assert usuario.last_login is None


def test_outro_email_continua_entrando_depois_do_limite_de_um_email(usuario):
    # Arrange
    Usuario.objects.create_user(
        OUTRO_EMAIL, SENHA, nome="Bruno Lima", matricula="2026002"
    )
    _esgotar_por_email()

    # Act
    resposta = _login(OUTRO_EMAIL, SENHA)

    # Assert
    assert resposta.status_code == 200


def test_email_com_caixa_e_espacos_diferentes_conta_como_o_mesmo(usuario):
    # Arrange
    for variacao in ["ANA@X.COM", " ana@x.com ", "Ana@X.com", "ana@X.COM ", EMAIL]:
        assert _login(variacao).status_code == 401

    # Act
    resposta = _login("  aNa@x.CoM")

    # Assert
    _assert_limite(resposta)


def test_limite_por_ip_vale_para_varios_emails():
    # Arrange
    for numero in range(LIMITE_POR_IP):
        assert _login(f"pessoa{numero}@x.com").status_code == 401

    # Act
    resposta = _login("mais.uma@x.com")

    # Assert
    _assert_limite(resposta)


def test_x_forwarded_for_diferente_nao_escapa_do_limite_por_ip():
    # Arrange
    for numero in range(LIMITE_POR_IP):
        resposta = _login(
            f"pessoa{numero}@x.com", HTTP_X_FORWARDED_FOR=f"10.0.0.{numero}"
        )
        assert resposta.status_code == 401

    # Act
    resposta = _login("mais.uma@x.com", HTTP_X_FORWARDED_FOR="10.0.0.200")

    # Assert
    _assert_limite(resposta)


@pytest.mark.parametrize(
    "corpo",
    [
        {"senha": "x"},
        {"email": "nao-e-email", "senha": "x"},
        {"email": 123, "senha": "x"},
        {"email": ["ana@x.com"], "senha": "x"},
        [{"email": "ana@x.com"}],
    ],
    ids=["sem-email", "email-invalido", "email-numero", "email-lista", "corpo-lista"],
)
def test_corpo_sem_email_utilizavel_cai_so_no_limite_por_ip(corpo):
    # Arrange
    cliente = APIClient()
    for _ in range(LIMITE_POR_IP):
        assert cliente.post(URL_LOGIN, corpo, format="json").status_code == 400

    # Act
    resposta = cliente.post(URL_LOGIN, corpo, format="json")

    # Assert
    _assert_limite(resposta)


def test_json_invalido_continua_400_e_conta_no_limite_por_ip():
    # Arrange
    cliente = APIClient()
    for _ in range(LIMITE_POR_IP):
        resposta = cliente.post(URL_LOGIN, "{", content_type="application/json")
        assert resposta.status_code == 400
        assert resposta.data["erro"]["codigo"] == "JSON_INVALIDO"

    # Act
    resposta = _login()

    # Assert
    _assert_limite(resposta)


def test_cadastro_acima_do_limite_por_ip_responde_429():
    # Arrange
    cliente = APIClient()
    for _ in range(LIMITE_DE_CADASTRO):
        assert cliente.post(URL_CADASTRO, {}, format="json").status_code == 400

    # Act
    resposta = cliente.post(URL_CADASTRO, {}, format="json")

    # Assert
    assert resposta.status_code == 429
    assert resposta.data["erro"] == {
        "codigo": "LIMITE_DE_TENTATIVAS",
        "mensagem": "Muitas tentativas. Tente de novo em 3600 segundos.",
    }
    assert resposta["Retry-After"] == "3600"


def test_depois_da_janela_o_login_volta_a_ser_aceito(usuario, relogio):
    # Arrange
    _esgotar_por_email()
    relogio.avancar(59)
    assert _login(senha=SENHA).status_code == 429
    relogio.avancar(1)

    # Act
    resposta = _login(senha=SENHA)

    # Assert
    assert resposta.status_code == 200


def test_espera_informada_diminui_com_o_tempo(usuario, relogio):
    # Arrange
    _esgotar_por_email()
    relogio.avancar(45)

    # Act
    resposta = _login()

    # Assert
    assert resposta.status_code == 429
    assert resposta.data["erro"]["mensagem"] == (
        "Muitas tentativas. Tente de novo em 15 segundos."
    )
    assert resposta["Retry-After"] == "15"


def test_taxas_vem_das_settings_a_cada_requisicao(usuario, settings):
    # Arrange
    settings.LIMITE_LOGIN_POR_EMAIL = "2/min"
    _login()
    _login()

    # Act
    resposta = _login()

    # Assert
    _assert_limite(resposta)


def test_resposta_429_nao_revela_o_limite_nem_se_o_email_existe(usuario):
    # Arrange
    _esgotar_por_email(EMAIL)
    _esgotar_por_email("ninguem@x.com")

    # Act
    da_conta = _login(EMAIL)
    sem_conta = _login("ninguem@x.com")

    # Assert
    assert da_conta.status_code == sem_conta.status_code == 429
    assert da_conta.data == sem_conta.data
    assert set(da_conta.data["erro"]) == {"codigo", "mensagem"}
    mensagem = da_conta.data["erro"]["mensagem"].lower()
    assert not any(termo in mensagem for termo in ("e-mail", "ip", "conta", "limite"))


@pytest.fixture
def redis_fora_do_ar(settings):
    settings.CACHES = {
        "default": {**settings.CACHES["default"], "LOCATION": REDIS_FORA_DO_AR}
    }


def test_redis_fora_do_ar_recusa_o_login_com_503_sem_conferir_a_senha(
    usuario, redis_fora_do_ar
):
    # Act
    resposta = _login(senha=SENHA)

    # Assert
    assert resposta.status_code == 503
    assert resposta.data == SERVICO_INDISPONIVEL
    usuario.refresh_from_db()
    assert usuario.last_login is None


def test_redis_fora_do_ar_recusa_o_cadastro_com_503(redis_fora_do_ar):
    # Act
    resposta = APIClient().post(
        URL_CADASTRO,
        {
            "nome": "Davi Rocha",
            "matricula": "2026099",
            "email": "davi@x.com",
            "senha": SENHA,
        },
        format="json",
    )

    # Assert
    assert resposta.status_code == 503
    assert resposta.data == SERVICO_INDISPONIVEL
    assert not Usuario.objects.filter(email="davi@x.com").exists()


def test_renovar_o_token_nao_tem_limite_de_tentativas(usuario):
    # Arrange
    refresh = _login(senha=SENHA).data["dados"]["refresh"]
    cliente = APIClient()

    # Act
    respostas = [
        cliente.post(URL_REFRESH, {"refresh": refresh}, format="json")
        for _ in range(LIMITE_POR_IP + 10)
    ]

    # Assert
    assert {resposta.status_code for resposta in respostas} == {200}


def _requisicao(email=EMAIL):
    return SimpleNamespace(
        data={"email": email}, headers={}, META={"REMOTE_ADDR": "10.0.0.7"}
    )


def _tentar_ao_mesmo_tempo(limite_da_classe, quantidade):
    barreira = threading.Barrier(quantidade)
    resultados = []

    def tentar():
        barreira.wait()
        resultados.append(limite_da_classe().allow_request(_requisicao(), None))

    threads = [threading.Thread(target=tentar) for _ in range(quantidade)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return resultados


@pytest.mark.parametrize(
    ("limite_da_classe", "limite", "quantidade"),
    [
        (LimiteDeLoginPorEmail, LIMITE_POR_EMAIL, 30),
        (LimiteDeLoginPorIp, LIMITE_POR_IP, 40),
    ],
    ids=["por-email", "por-ip"],
)
def test_tentativas_simultaneas_nao_passam_do_limite(
    limite_da_classe, limite, quantidade
):
    # Act
    resultados = _tentar_ao_mesmo_tempo(limite_da_classe, quantidade)

    # Assert
    assert len(resultados) == quantidade
    assert resultados.count(True) == limite
    assert resultados.count(False) == quantidade - limite


def test_espera_com_limite_reduzido_e_a_da_tentativa_que_libera_a_vaga(
    usuario, relogio, settings
):
    # Arrange
    for _ in range(LIMITE_POR_EMAIL):
        assert _login().status_code == 401
        relogio.avancar(1)
    relogio.avancar(-1)
    settings.LIMITE_LOGIN_POR_EMAIL = "2/min"

    # Act
    resposta = _login()

    # Assert
    assert resposta.status_code == 429
    assert resposta.data["erro"]["mensagem"] == (
        "Muitas tentativas. Tente de novo em 59 segundos."
    )
    assert resposta["Retry-After"] == "59"
