import runpy
from pathlib import Path

import pytest
from django.core.exceptions import ImproperlyConfigured

CAMINHO_DO_SETTINGS = Path(__file__).resolve().parent.parent / "settings.py"
CHAVE_FORTE = "k7Qp2Zx9VbN4mL8sT1wE5rY3uI6oA0dF" + "hJ2gC4vB7nM9xZ1aS3dF5gH7jK9lP"
CHAVE_DO_EXEMPLO = "troque-esta-chave-por-uma-com-pelo-menos-32-caracteres"
VARIAVEIS_DE_PRODUCAO = {
    "DJANGO_MODO_PRODUCAO": "1",
    "DJANGO_DEBUG": "False",
    "DJANGO_SECRET_KEY": CHAVE_FORTE,
    "DJANGO_ALLOWED_HOSTS": "sistema.exemplo.com",
    "DB_HOST": "db",
}
OPCIONAIS = (
    "DJANGO_MODO_PRODUCAO",
    "DJANGO_DEBUG",
    "DJANGO_ALLOWED_HOSTS",
    "DJANGO_HTTPS",
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "DJANGO_NUM_PROXIES",
    "DB_HOST",
    "CORS_ALLOWED_ORIGINS",
)


def carregar(monkeypatch, **variaveis):
    for nome in OPCIONAIS:
        monkeypatch.delenv(nome, raising=False)
    base = {
        "DJANGO_SECRET_KEY": CHAVE_DO_EXEMPLO,
        "DB_DATABASE": "banco",
        "DB_USER": "usuario",
        "DB_PASSWORD": "senha",
        "REDIS_URL": "redis://redis:6379/0",
    }
    for nome, valor in {**base, **variaveis}.items():
        monkeypatch.setenv(nome, valor)
    return runpy.run_path(str(CAMINHO_DO_SETTINGS))


def producao(monkeypatch, **mudancas):
    variaveis = {**VARIAVEIS_DE_PRODUCAO, **mudancas}
    for nome, valor in list(variaveis.items()):
        if valor is None:
            del variaveis[nome]
            monkeypatch.delenv(nome, raising=False)
    return carregar(monkeypatch, **variaveis)


def test_sem_a_variavel_do_modo_de_producao_a_chave_de_exemplo_e_aceita(monkeypatch):
    # Act
    cfg = carregar(monkeypatch)

    # Assert
    assert cfg["MODO_DE_PRODUCAO"] is False
    assert cfg["SECRET_KEY"] == CHAVE_DO_EXEMPLO
    assert cfg["DEBUG"] is False


def test_sem_a_variavel_do_modo_de_producao_o_banco_tem_host_padrao(monkeypatch):
    # Act
    cfg = carregar(monkeypatch)

    # Assert
    assert cfg["DATABASES"]["default"]["HOST"] == "db"


def test_sem_a_variavel_do_modo_de_producao_nada_de_producao_e_ligado(monkeypatch):
    # Act
    cfg = carregar(monkeypatch, DJANGO_DEBUG="True")

    # Assert
    assert cfg["DEBUG"] is True
    assert "whitenoise.middleware.WhiteNoiseMiddleware" not in cfg["MIDDLEWARE"]
    assert "STORAGES" not in cfg
    assert cfg["REST_FRAMEWORK"]["NUM_PROXIES"] == 0
    assert cfg["CSRF_TRUSTED_ORIGINS"] == []


@pytest.mark.parametrize(
    "opcao",
    [
        "SECURE_SSL_REDIRECT",
        "SECURE_HSTS_SECONDS",
        "SESSION_COOKIE_SECURE",
        "CSRF_COOKIE_SECURE",
        "SECURE_PROXY_SSL_HEADER",
    ],
)
def test_sem_https_nenhuma_opcao_de_https_e_definida(monkeypatch, opcao):
    # Act
    cfg = carregar(monkeypatch)

    # Assert
    assert opcao not in cfg


def test_estaticos_do_admin_tem_destino_do_collectstatic_em_qualquer_modo(monkeypatch):
    # Act
    cfg = carregar(monkeypatch)

    # Assert
    assert cfg["STATIC_ROOT"] == CAMINHO_DO_SETTINGS.parent.parent / "staticfiles"


def test_producao_com_tudo_definido_carrega(monkeypatch):
    # Act
    cfg = producao(monkeypatch)

    # Assert
    assert cfg["MODO_DE_PRODUCAO"] is True
    assert cfg["SECRET_KEY"] == CHAVE_FORTE
    assert cfg["ALLOWED_HOSTS"] == ["sistema.exemplo.com"]
    assert cfg["DEBUG"] is False


def test_producao_liga_o_whitenoise_logo_depois_do_security_middleware(monkeypatch):
    # Act
    middleware = producao(monkeypatch)["MIDDLEWARE"]

    # Assert
    seguranca = middleware.index("django.middleware.security.SecurityMiddleware")
    assert middleware[seguranca + 1] == "whitenoise.middleware.WhiteNoiseMiddleware"


def test_producao_serve_os_estaticos_com_manifesto_e_compressao(monkeypatch):
    # Act
    storages = producao(monkeypatch)["STORAGES"]

    # Assert
    assert storages["staticfiles"]["BACKEND"] == (
        "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )


@pytest.mark.parametrize(
    "variavel", ["DJANGO_SECRET_KEY", "DB_DATABASE", "DB_USER", "DB_PASSWORD"]
)
def test_producao_sem_segredo_obrigatorio_falha_citando_a_variavel(
    monkeypatch, variavel
):
    # Arrange
    cfg_valida = {**VARIAVEIS_DE_PRODUCAO}
    carregar(monkeypatch, **cfg_valida, **{"DB_DATABASE": "b"})
    monkeypatch.delenv(variavel)

    # Act / Assert
    with pytest.raises(ImproperlyConfigured, match=variavel):
        runpy.run_path(str(CAMINHO_DO_SETTINGS))


def test_producao_sem_host_do_banco_falha_citando_a_variavel(monkeypatch):
    # Act / Assert
    with pytest.raises(ImproperlyConfigured, match="DB_HOST"):
        producao(monkeypatch, DB_HOST=None)


def test_producao_sem_hosts_permitidos_falha_citando_a_variavel(monkeypatch):
    # Act / Assert
    with pytest.raises(ImproperlyConfigured, match="DJANGO_ALLOWED_HOSTS"):
        producao(monkeypatch, DJANGO_ALLOWED_HOSTS=None)


def test_producao_nao_aceita_qualquer_host(monkeypatch):
    # Act / Assert
    with pytest.raises(ImproperlyConfigured, match="DJANGO_ALLOWED_HOSTS"):
        producao(monkeypatch, DJANGO_ALLOWED_HOSTS="sistema.exemplo.com,*")


def test_producao_nao_aceita_a_chave_de_exemplo(monkeypatch):
    # Act / Assert
    with pytest.raises(ImproperlyConfigured, match="DJANGO_SECRET_KEY"):
        producao(monkeypatch, DJANGO_SECRET_KEY=CHAVE_DO_EXEMPLO)


@pytest.mark.parametrize(
    "chave",
    ["curta", "a" * 80, "django-insecure-" + "xK9" * 20, "troque-" + "xK9pQ" * 12],
    ids=["curta", "poucos-diferentes", "prefixo-do-django", "prefixo-de-exemplo"],
)
def test_producao_nao_aceita_chave_fraca(monkeypatch, chave):
    # Act / Assert
    with pytest.raises(ImproperlyConfigured, match="DJANGO_SECRET_KEY"):
        producao(monkeypatch, DJANGO_SECRET_KEY=chave)


def test_producao_com_cinquenta_caracteres_e_aceita(monkeypatch):
    # Arrange
    chave = CHAVE_FORTE[:50]

    # Act
    cfg = producao(monkeypatch, DJANGO_SECRET_KEY=chave)

    # Assert
    assert cfg["SECRET_KEY"] == chave


def test_producao_com_debug_ligado_falha(monkeypatch):
    # Act / Assert
    with pytest.raises(ImproperlyConfigured, match="DJANGO_DEBUG"):
        producao(monkeypatch, DJANGO_DEBUG="True")


def test_https_ligado_define_exatamente_as_opcoes_documentadas(monkeypatch):
    # Act
    cfg = producao(monkeypatch, DJANGO_HTTPS="1")

    # Assert
    assert cfg["SECURE_SSL_REDIRECT"] is True
    assert cfg["SECURE_REDIRECT_EXEMPT"] == [r"^api/health/$"]
    assert cfg["SECURE_HSTS_SECONDS"] == 31536000
    assert cfg["SECURE_HSTS_INCLUDE_SUBDOMAINS"] is True
    assert cfg["SECURE_HSTS_PRELOAD"] is True
    assert cfg["SESSION_COOKIE_SECURE"] is True
    assert cfg["CSRF_COOKIE_SECURE"] is True
    assert cfg["SECURE_PROXY_SSL_HEADER"] == ("HTTP_X_FORWARDED_PROTO", "https")


def test_https_desligado_explicitamente_nao_define_nada(monkeypatch):
    # Act
    cfg = producao(monkeypatch, DJANGO_HTTPS="0")

    # Assert
    assert "SECURE_SSL_REDIRECT" not in cfg
    assert "SESSION_COOKIE_SECURE" not in cfg


def test_o_https_tambem_pode_ser_ligado_fora_do_modo_de_producao(monkeypatch):
    # Act
    cfg = carregar(monkeypatch, DJANGO_HTTPS="true")

    # Assert
    assert cfg["SECURE_SSL_REDIRECT"] is True


def test_origens_confiaveis_do_csrf_vem_da_variavel(monkeypatch):
    # Act
    cfg = producao(
        monkeypatch,
        DJANGO_CSRF_TRUSTED_ORIGINS="https://a.exemplo.com, https://b.exemplo.com",
    )

    # Assert
    assert cfg["CSRF_TRUSTED_ORIGINS"] == [
        "https://a.exemplo.com",
        "https://b.exemplo.com",
    ]


def test_numero_de_proxies_vem_da_variavel(monkeypatch):
    # Act
    cfg = producao(monkeypatch, DJANGO_NUM_PROXIES="1")

    # Assert
    assert cfg["REST_FRAMEWORK"]["NUM_PROXIES"] == 1


def test_numero_de_proxies_invalido_impede_a_subida(monkeypatch):
    # Act / Assert
    with pytest.raises(ImproperlyConfigured, match="DJANGO_NUM_PROXIES"):
        producao(monkeypatch, DJANGO_NUM_PROXIES="um")
