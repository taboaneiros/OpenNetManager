from __future__ import annotations

from pathlib import Path
import environ

# 1. Configuração de caminhos base
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Inicialização do django-environ com os esquemas/defaults combinados
env = environ.Env(
    DEBUG=(bool, False),
    CACHE_TIMEOUT=(int, 60),
    SSH_TIMEOUT=(int, 10),
    SSH_RETRIES=(int, 2),
    COLLECT_INTERVAL_SECONDS=(int, 300),
)
environ.Env.read_env(BASE_DIR / ".env")

# 3. Configurações essenciais de Segurança e Debug
DEBUG = env.bool("DEBUG", default=True)
SECRET_KEY = env("SECRET_KEY", default="django-insecure-opennetmanager-dev")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["0.0.0.0","127.0.0.1", "localhost"])

# 4. Definição de Aplicações (União das listas de apps sem duplicatas)
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.authentication",
    "apps.dashboard",
    "apps.devices",
    "apps.monitoring",
    "apps.api",
]

# 5. Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 6. Roteamento e WSGI/ASGI
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# 7. Templates (Incluindo os context_processors de ambos)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# 8. Banco de Dados (Mantida a lógica flexível de checagem Postgres/SQLite)
DB_ENGINE = env("DB_ENGINE", default="sqlite")
if DB_ENGINE == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST", default="localhost"),
            "PORT": env("DB_PORT", default="5432"),
        }
    }
else:
    # Fallback para o env.db ou caminho manual estruturado
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / env("DB_NAME", default="db.sqlite3"),
        }
    }

# 9. Validadores de Senha
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
]

# 10. Internacionalização e Fuso Horário
LANGUAGE_CODE = env("LANGUAGE_CODE", default="pt-br")
TIME_ZONE = env("TIME_ZONE", default="America/Sao_Paulo")
USE_I18N = True
USE_TZ = True

# 11. Arquivos Estáticos e de Mídia
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 12. Sistema de Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "opennetmanager-cache",
        "TIMEOUT": env("CACHE_TIMEOUT"),
    }
}

# 13. Django Rest Framework (DRF)
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
}

# 14. Configurações de Log (Criação automática do diretório inclusa)
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        }
    },
    "handlers": {
        "application_file": {
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "application.log",
            "formatter": "standard",
            "level": "INFO",
        },
        "error_file": {
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "error.log",
            "formatter": "standard",
            "level": "ERROR",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "application_file", "error_file"],
            "level": "INFO",
            "propagate": True,
        }
    },
}

# 15. Parâmetros específicos da aplicação (SSH, Coleta e Autenticação)
SSH_TIMEOUT = env("SSH_TIMEOUT", default=10)
SSH_RETRIES = env("SSH_RETRIES", default=2)
SSH_ENCODING = env("SSH_ENCODING", default="utf-8")
COLLECT_INTERVAL_SECONDS = env("COLLECT_INTERVAL_SECONDS", default=300)
DEFAULT_SSH_USERNAME = env("DEFAULT_SSH_USERNAME", default="admin")
DEFAULT_SSH_PASSWORD = env("DEFAULT_SSH_PASSWORD", default="changeme")

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/auth/login/"
