"""
Django settings for risk_module project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

import environ
from celery.schedules import crontab
from django.utils.log import DEFAULT_LOGGING

from risk_module import sentry

env = environ.Env(
    # Application info
    RISK_ENVIRONMENT=str,
    RISK_API_FQDN=str,
    # Django configs
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=str,
    DJANGO_ALLOWED_HOSTS=(list, ["*"]),
    TIME_ZONE=(str, "UTC"),
    # Database
    DATABASE_NAME=str,
    DATABASE_USER=str,
    DATABASE_PASSWORD=str,
    DATABASE_PORT=int,
    DATABASE_HOST=str,
    # S3 (NOTE: Not used anywhere)
    USE_AWS_FOR_MEDIA=(bool, False),
    S3_AWS_ACCESS_KEY_ID=str,
    S3_AWS_SECRET_ACCESS_KEY=str,
    S3_STORAGE_BUCKET_NAME=str,
    S3_REGION_NAME=str,
    # Redis
    CELERY_REDIS_URL=str,  # redis://redis:6379/0
    CACHE_REDIS_URL=str,  # redis://redis:6379/1
    # Sentry
    SENTRY_DSN=(str, None),
    SENTRY_TRACE_SAMPLE_RATE=(float, 0.2),
    SENTRY_PROFILE_SAMPLE_RATE=(float, 0.2),
    # PDC
    PDC_USERNAME=str,
    PDC_PASSWORD=str,
    PDC_ACCESS_TOKEN=str,
    # Meteoswiss
    METEOSWISS_S3_ENDPOINT_URL=str,
    METEOSWISS_S3_BUCKET=str,
    METEOSWISS_S3_ACCESS_KEY=str,
    METEOSWISS_S3_SECRET_KEY=str,
    # Logging
    APPS_LOGGING_LEVEL=(str, "WARNING"),
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = env("DJANGO_DEBUG")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ["server", *env("DJANGO_ALLOWED_HOSTS")]


# Application definition

INSTALLED_APPS = [
    # LOCAL APPS
    "imminent",
    "seasonal",
    "common",
    # LIBRARIES
    "rest_framework",
    "django_filters",
    "django_celery_beat",
    "corsheaders",
    "storages",
    "drf_spectacular",
    #  Health-check
    "health_check",  # required
    "health_check.db",  # stock Django health checkers
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.migrations",
    "health_check.contrib.psutil",  # disk and memory utilization; requires psutil
    "health_check.contrib.redis",  # requires Redis broker
    # DJANGO APPS
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
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

ROOT_URLCONF = "risk_module.urls"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "risk_module.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "PORT": env("DATABASE_PORT"),
        "HOST": env("DATABASE_HOST"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


def log_render_extra_context(record):
    """
    Append extra->context to logs
    """
    # NOTE: Using .__ to make sure this is not sent to sentry but .context is
    record.__context_message = ""
    if hasattr(record, "context"):
        record.__context_message = f" - {str(record.context)}"
    return True


LOGGING = {
    **DEFAULT_LOGGING,
    "formatters": {
        **DEFAULT_LOGGING["formatters"],
        "simple": {
            "format": "%(asctime)s %(levelname)s/%(processName)s - %(name)s - %(message)s%(__context_message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
    },
    "filters": {
        **DEFAULT_LOGGING["filters"],
        "render_extra_context": {
            "()": "django.utils.log.CallbackFilter",
            "callback": log_render_extra_context,
        },
    },
    "handlers": {
        **DEFAULT_LOGGING["handlers"],
        # Send all messages to console
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "filters": ["render_extra_context"],
        },
    },
    "loggers": {
        **DEFAULT_LOGGING["loggers"],
        "": {
            # This is the "catch all" logger
            # XXX: Does this work?
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": env("APPS_LOGGING_LEVEL"),
            "propagate": False,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = env("TIME_ZONE")

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


if env("USE_AWS_FOR_MEDIA"):
    AWS_S3_ACCESS_KEY_ID = env("S3_AWS_ACCESS_KEY_ID")
    AWS_S3_SECRET_ACCESS_KEY = env("S3_AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("S3_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = env("S3_REGION_NAME")

    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = "private"

    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

STATIC_ROOT = os.path.join(BASE_DIR, "storage/static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "storage/media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CELERY_REDIS_URL = env("CELERY_REDIS_URL")
CELERY_BROKER_URL = CELERY_REDIS_URL
CELERY_RESULT_BACKEND = CELERY_REDIS_URL
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACKS_LATE = True

# TODO: Need to disable one of the tasks which doesn't work
CELERY_BEAT_SCHEDULE = {
    "import_earthquake_data": {
        "task": "imminent.tasks.import_earthquake_data",
        "schedule": crontab(minute=0, hour=0),  # This task execute daily at 12 AM (UTC)
    },
    "create_pdc_data": {
        "task": "imminent.tasks.create_pdc_data",
        "schedule": crontab(minute=0, hour="*/2"),  # This task execute daily in 2 hours interval
    },
    "create_pdc_daily": {
        "task": "imminent.tasks.create_pdc_daily",
        "schedule": crontab(minute=0, hour="5"),  # This task execute daily at 5 AM (UTC)
    },
    "create_pdc_displacement": {
        "task": "imminent.tasks.create_pdc_displacement",
        "schedule": crontab(minute=0, hour="*/3"),  # This task execute daily in 3 hours interval
    },
    "create_pdc_polygon": {
        "task": "imminent.tasks.create_pdc_polygon",
        "schedule": crontab(minute=0, hour="*/6"),  # This task to execute daily in 6  interval
    },
    "create_pdc_intensity": {
        "task": "imminent.tasks.create_pdc_intensity",
        "schedule": crontab(minute=0, hour="*/7"),  # This task to execute daily in 7  interval
    },
    "check_pdc_status": {
        "task": "imminent.tasks.check_pdc_status",
        "schedule": crontab(minute=0, hour=1),  # This task to execute daily in 1 AM(UTC)
    },
    "create_pdc_three_days_cou": {
        "task": "imminent.tasks.create_pdc_three_days_cou",
        "schedule": crontab(minute=0, hour="*"),  # This task executes every hour
    },
    "create_pdc_five_days_cou": {
        "task": "imminent.tasks.create_pdc_five_days_cou",
        "schedule": crontab(minute=0, hour="*"),  # This task executes every hour
    },
    "create_hazard_information": {
        "task": "seasonal.tasks.import_think_hazard_informations",
        "schedule": crontab(0, 0, day_of_month="2"),  # This task execute at second day of every month
    },
    "create_adam_exposure": {
        "task": "imminent.tasks.create_adam_exposure",
        "schedule": crontab(minute=0, hour="*/4"),  # This task execute daily at 4 hours interval
    },
    "update_adam_cyclone": {
        "task": "imminent.tasks.update_adam_cyclone",
        "schedule": crontab(minute=0, hour="*/4"),  # This task execute daily at 4 hours interval
    },
    "import_gdacs_data": {
        "task": "imminent.tasks.import_gdacs_data",
        "schedule": crontab(minute=0, hour="*/4"),  # This task execute daily at 4 hours interval
    },
    "pull_meteoswiss": {
        "task": "imminent.tasks.pull_meteoswiss",
        "schedule": crontab(minute=0, hour="*/4"),  # This task execute daily at 4 hours interval
    },
    "pull_meteoswiss_geo": {
        "task": "imminent.tasks.pull_meteoswiss_geo",
        "schedule": crontab(minute=0, hour="*/4"),  # This task execute daily at 4 hours interval
    },
    "meteoswiss_agg": {
        "task": "imminent.tasks.meteoswiss_agg",
        "schedule": crontab(minute=0, hour="*/4"),  # This task execute daily at 4 hours interval
    },
    "update_adam_alert_level": {
        "task": "imminent.tasks.update_adam_alert_level",
        "schedule": crontab(minute=0, hour="*/4"),  # This task execute daily at 4 hours interval
    },
}

CORS_ORIGIN_ALLOW_ALL = True

# NOTE: This is experimental distance in km
# Can be changed
BUFFER_DISTANCE_IN_KM = 50

# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# ENDPOINT_URL = os.environ['ENDPOINT_URL']
# Sentry Config
SENTRY_DSN = env("SENTRY_DSN")
SENTRY_TRACE_SAMPLE_RATE = env("SENTRY_TRACE_SAMPLE_RATE")
SENTRY_PROFILE_SAMPLE_RATE = env("SENTRY_PROFILE_SAMPLE_RATE")
RISK_ENVIRONMENT = env("RISK_ENVIRONMENT")
RISK_API_FQDN = env("RISK_API_FQDN")

SENTRY_CONFIG = {
    "dsn": SENTRY_DSN,
    "send_default_pii": True,
    "traces_sample_rate": SENTRY_TRACE_SAMPLE_RATE,
    "profiles_sample_rate": SENTRY_PROFILE_SAMPLE_RATE,
    "release": sentry.fetch_git_sha(BASE_DIR),
    "environment": RISK_ENVIRONMENT,
    "debug": DEBUG,
    "tags": {
        "site": RISK_API_FQDN,
    },
}
if SENTRY_DSN:
    sentry.init_sentry(
        app_type="API",
        **SENTRY_CONFIG,
    )

SPECTACULAR_SETTINGS = {
    "TITLE": "IFRC-GO RISK API",
    "DESCRIPTION": "IFRC-GO RISK API Documenation",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# Health-check config
REDIS_URL = env("CACHE_REDIS_URL")
HEALTHCHECK_CACHE_KEY = "go_risk_healthcheck_key"
HEALTH_CHECK = {
    "DISK_USAGE_MAX": 80,  # percent
    "MEMORY_MIN": 100,  # in MB
}

# Cache

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "dj_cache-",
    }
}

# Redis locking
REDIS_DEFAULT_LOCK_EXPIRE = 60 * 10  # Lock expires in 10min (in seconds)

# PDC
PDC_USERNAME = env("PDC_USERNAME")
PDC_PASSWORD = env("PDC_PASSWORD")
PDC_ACCESS_TOKEN = env("PDC_ACCESS_TOKEN")

# METEO_SWISS
METEO_SWISS_S3_ENDPOINT_URL = env("METEOSWISS_S3_ENDPOINT_URL")
METEO_SWISS_S3_BUCKET = env("METEOSWISS_S3_BUCKET")
METEO_SWISS_S3_ACCESS_KEY = env("METEOSWISS_S3_ACCESS_KEY")
METEO_SWISS_S3_SECRET_KEY = env("METEOSWISS_S3_SECRET_KEY")

# Static configs - TODO: django settings don't have a type support, maybe define this somewhere else?
WFP_ADAM = "https://exie6ocssxnczub3aslzanna540gfdjs.lambda-url.eu-west-1.on.aws"
