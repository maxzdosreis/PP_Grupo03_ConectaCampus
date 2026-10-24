import os
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


def _lista(nome):
    return [
        item.strip() for item in os.environ.get(nome, "").split(",") if item.strip()
    ]


SECRET_KEY = _obrigatoria("DJANGO_SECRET_KEY")
DEBUG = _booleano("DJANGO_DEBUG")
ALLOWED_HOSTS = _lista("DJANGO_ALLOWED_HOSTS")
CORS_ALLOWED_ORIGINS = _lista("CORS_ALLOWED_ORIGINS")

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
    "espacos",
    "reservas",
    "contas",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
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
        "HOST": os.environ.get("DB_HOST", "db"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "OPTIONS": {"connect_timeout": 5},
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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

_RENDERIZADORES = ["rest_framework.renderers.JSONRenderer"]
if DEBUG:
    _RENDERIZADORES.append("rest_framework.renderers.BrowsableAPIRenderer")

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": _RENDERIZADORES,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "EXCEPTION_HANDLER": "compartilhado.api.tratador_de_erros.tratar_excecao",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=_inteiro("JWT_ACCESS_MINUTES", 30)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=_inteiro("JWT_REFRESH_DAYS", 1)),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
}
