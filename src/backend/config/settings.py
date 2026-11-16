import os
import re
from datetime import timedelta
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def _obrigatoria(nome):
    valor = os.environ.get(nome, "").strip()
    if not valor:
        raise ImproperlyConfigured(
            f"A variável de ambiente {nome} não está definida. "
            "Copie src/.env.example para src/.env e preencha o valor."
        )
    return valor


def _booleano(nome, padrao=False):
    valor = os.environ.get(nome)
    if valor is None:
        return padrao
    return valor.strip().lower() in {"1", "true", "sim", "yes", "on"}


def _inteiro(nome, padrao):
    valor = os.environ.get(nome, "").strip()
    if not valor:
        return padrao
    try:
        return int(valor)
    except ValueError:
        raise ImproperlyConfigured(
            f"A variável de ambiente {nome} precisa ser um número inteiro."
        ) from None


def _taxa(nome, padrao):
    valor = os.environ.get(nome, "").strip() or padrao
    if not re.fullmatch(r"[1-9]\d*/(s|min|hour|day)", valor):
        raise ImproperlyConfigured(
            f"A variável de ambiente {nome} precisa estar no formato N/período, "
            "com N inteiro positivo e período s, min, hour ou day "
            f"(ex.: {padrao})."
        )
    return valor


def _redis_url():
    valor = os.environ.get("REDIS_URL", "").strip()
    if not valor:
        raise ImproperlyConfigured(
            "A variável de ambiente REDIS_URL não está definida. Ela vem do "
            "docker-compose.yml: suba o backend com docker compose up."
        )
    return valor


def _lista(nome):
    return [
        item.strip() for item in os.environ.get(nome, "").split(",") if item.strip()
    ]


def _exigir_configuracao_de_producao(chave, debug, hosts, host_do_banco):
    if debug:
        raise ImproperlyConfigured(
            "DJANGO_DEBUG precisa ser False no modo de produção (DJANGO_MODO_PRODUCAO)."
        )
    if (
        len(chave) < _TAMANHO_MINIMO_DA_CHAVE
        or len(set(chave)) < 5
        or chave.startswith(_PREFIXOS_DE_CHAVE_DE_EXEMPLO)
    ):
        raise ImproperlyConfigured(
            f"DJANGO_SECRET_KEY precisa ter pelo menos {_TAMANHO_MINIMO_DA_CHAVE} "
            "caracteres aleatórios e não pode ser a chave de exemplo no modo de "
            "produção. Gere uma com: "
            'python -c "import secrets; print(secrets.token_urlsafe(64))"'
        )
    if not hosts or "*" in hosts:
        raise ImproperlyConfigured(
            "DJANGO_ALLOWED_HOSTS precisa listar os hosts do sistema (sem '*') no "
            "modo de produção."
        )
    if not host_do_banco:
        raise ImproperlyConfigured(
            "A variável de ambiente DB_HOST não está definida (obrigatória no modo "
            "de produção)."
        )


_TAMANHO_MINIMO_DA_CHAVE = 50
_PREFIXOS_DE_CHAVE_DE_EXEMPLO = ("troque-", "django-insecure-")

MODO_DE_PRODUCAO = _booleano("DJANGO_MODO_PRODUCAO")

SECRET_KEY = _obrigatoria("DJANGO_SECRET_KEY")
DEBUG = _booleano("DJANGO_DEBUG")
ALLOWED_HOSTS = _lista("DJANGO_ALLOWED_HOSTS")
CORS_ALLOWED_ORIGINS = _lista("CORS_ALLOWED_ORIGINS")
_HOST_DO_BANCO = (
    os.environ.get("DB_HOST", "").strip()
    if MODO_DE_PRODUCAO
    else os.environ.get("DB_HOST", "db")
)
if MODO_DE_PRODUCAO:
    _exigir_configuracao_de_producao(SECRET_KEY, DEBUG, ALLOWED_HOSTS, _HOST_DO_BANCO)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "rest_framework",
    "corsheaders",
    "rest_framework_simplejwt.token_blacklist",
    "espacos",
    "reservas",
    "contas",
    "exemplos",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    *(["whitenoise.middleware.WhiteNoiseMiddleware"] if MODO_DE_PRODUCAO else []),
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _obrigatoria("DB_DATABASE"),
        "USER": _obrigatoria("DB_USER"),
        "PASSWORD": _obrigatoria("DB_PASSWORD"),
        "HOST": _HOST_DO_BANCO,
        "PORT": os.environ.get("DB_PORT", "5432"),
        "OPTIONS": {"connect_timeout": 5},
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": _redis_url(),
        "KEY_PREFIX": "conecta-campus",
        "OPTIONS": {"socket_connect_timeout": 1, "socket_timeout": 1},
    }
}

AUTH_USER_MODEL = "contas.Usuario"

MIGRATION_MODULES = {
    app: f"{app}.infrastructure.migrations" for app in ("espacos", "reservas", "contas")
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {"user_attributes": ("email", "nome", "matricula")},
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

if MODO_DE_PRODUCAO:
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        },
    }

if _booleano("DJANGO_HTTPS"):
    SECURE_SSL_REDIRECT = True
    SECURE_REDIRECT_EXEMPT = [r"^api/health/$"]  # o healthcheck chega por HTTP
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = _lista("DJANGO_CSRF_TRUSTED_ORIGINS")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

_RENDERIZADORES = ["rest_framework.renderers.JSONRenderer"]
if DEBUG:
    _RENDERIZADORES.append("rest_framework.renderers.BrowsableAPIRenderer")

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": _RENDERIZADORES,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "EXCEPTION_HANDLER": "compartilhado.api.tratador_de_erros.tratar_excecao",
    # Quantos proxies confiáveis ficam na frente (o nginx do modo de produção conta 1).
    "NUM_PROXIES": _inteiro("DJANGO_NUM_PROXIES", 0),
}

LIMITE_LOGIN_POR_EMAIL = _taxa("LIMITE_LOGIN_POR_EMAIL", "5/min")
LIMITE_LOGIN_POR_IP = _taxa("LIMITE_LOGIN_POR_IP", "20/min")
LIMITE_CADASTRO_POR_IP = _taxa("LIMITE_CADASTRO_POR_IP", "10/hour")
LIMITE_TROCA_DE_SENHA_POR_USUARIO = _taxa("LIMITE_TROCA_DE_SENHA_POR_USUARIO", "5/min")
LIMITE_GESTAO_DE_USUARIOS_POR_USUARIO = _taxa(
    "LIMITE_GESTAO_DE_USUARIOS_POR_USUARIO", "30/min"
)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=_inteiro("JWT_ACCESS_MINUTES", 30)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=_inteiro("JWT_REFRESH_DAYS", 1)),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}
