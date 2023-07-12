"""
Django settings for risk_module project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import environ
from pathlib import Path
from celery.schedules import crontab

from risk_module import sentry


env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=str,
    DJANGO_ALLOWED_HOSTS=(list, ['*']),
    # Database
    DATABASE_NAME=str,
    DATABASE_USER=str,
    DATABASE_PASSWORD=str,
    DATABASE_PORT=(int, 5432),
    DATABASE_HOST=str,
    TIME_ZONE=(str, 'UTC'),

    USE_AWS_FOR_MEDIA=(bool, False),
    S3_AWS_ACCESS_KEY_ID=str,
    S3_AWS_SECRET_ACCESS_KEY=str,
    S3_STORAGE_BUCKET_NAME=str,
    S3_REGION_NAME=str,

    CELERY_REDIS_URL=str,

    SENTRY_DSN=(str, None),
    SENTRY_SAMPLE_RATE=(float, 0.2),
    RISK_ENVIRONMENT=(str, 'local'),
    RISK_API_FQDN=(str, 'localhost'),

)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DJANGO_SECRET_KEY')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['server', *env('DJANGO_ALLOWED_HOSTS')]


# Application definition

INSTALLED_APPS = [
    # LOCAL APPS
    'imminent',
    'seasonal',
    'common',

    # LIBRARIES
    'rest_framework',
    'django_filters',
    'django_celery_beat',
    'corsheaders',
    'storages',
    'drf_spectacular',

    # DJANGO APPS
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'risk_module.urls'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'risk_module.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'PORT': env('DATABASE_PORT'),
        'HOST': env('DATABASE_HOST'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '[contactor] %(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        # Send all messages to console
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        # This is the "catch all" logger
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = env('TIME_ZONE')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


if env('USE_AWS_FOR_MEDIA'):
    AWS_S3_ACCESS_KEY_ID = env('S3_AWS_ACCESS_KEY_ID')
    AWS_S3_SECRET_ACCESS_KEY = env('S3_AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('S3_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = env('S3_REGION_NAME')

    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = 'private'

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
STATIC_URL = "/staticfiles/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CELERY_REDIS_URL = env('CELERY_REDIS_URL')
CELERY_BROKER_URL = CELERY_REDIS_URL
CELERY_RESULT_BACKEND = CELERY_REDIS_URL
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACKS_LATE = True

CELERY_BEAT_SCHEDULE = {
    "import_earthquake_data": {
        "task": "imminent.tasks.import_earthquake_data",
        "schedule": crontab(minute=0, hour=0),  # This task execute daily at 12 AM (UTC)
    },
    "create_pdc_data": {
        "task": "imminent.tasks.create_pdc_data",
        "schedule": crontab(minute=0, hour='*/2'),  # This task execute daily in 2 hours interval
    },
    "create_pdc_daily": {
        "task": "imminent.tasks.create_pdc_daily",
        "schedule": crontab(minute=0, hour='5'),  # This task execute daily at 5 AM (UTC)
    },
    "create_pdc_displacement": {
        "task": "imminent.tasks.create_pdc_displacement",
        "schedule": crontab(minute=0, hour='*/3'),  # This task execute daily in 3 hours interval
    },
    "create_pdc_polygon": {
        "task": "imminent.tasks.create_pdc_polygon",
        "schedule": crontab(minute=0, hour='*/6')  # This task to execute daily in 6  interval
    },
    "create_pdc_intensity": {
        "task": "imminent.tasks.create_pdc_intensity",
        "schedule": crontab(minute=0, hour='*/7')  # This task to execute daily in 7  interval
    },
    "check_pdc_status": {
        "task": "imminent.tasks.check_pdc_status",
        "schedule": crontab(minute=0, hour=1)  # This task to execute daily in 1 AM(UTC)
    },
    "create_hazard_information": {
        "task": "seasonal.tasks.import_think_hazard_informations",
        "schedule": crontab(0, 0, day_of_month='2')  # This task execute at second day of every month
    },
    "create_adam_exposure": {
        "task": "imminent.tasks.create_adam_exposure",
        "schedule": crontab(minute=0, hour='*/4')  # This task execute daily at 4 hours interval
    },
    "update_adam_cyclone": {
        "task": "imminent.tasks.update_adam_cyclone",
        "schedule": crontab(minute=0, hour='*/4')  # This task execute daily at 4 hours interval
    },
    "import_gdacs_data": {
        "task": "imminent.tasks.import_gdacs_data",
        "schedule": crontab(minute=0, hour='*/4')  # This task execute daily at 4 hours interval
    },
    "pull_meteoswiss": {
        "task": "imminent.tasks.pull_meteoswiss",
        "schedule": crontab(minute=0, hour='*/4')  # This task execute daily at 4 hours interval
    },
    "meteoswiss_agg": {
        "task": "imminent.tasks.meteoswiss_agg",
        "schedule": crontab(minute=0, hour='*/4')  # This task execute daily at 4 hours interval
    },
    "update_adam_alert_level": {
        "task": "imminent.tasks.update_adam_alert_level",
        "schedule": crontab(minute=0, hour='*/4')  # This task execute daily at 4 hours interval
    }
}

CORS_ORIGIN_ALLOW_ALL = True

# NOTE: This is experimental distance in km
# Can be changed
BUFFER_DISTANCE_IN_KM = 50

# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
# ENDPOINT_URL = os.environ['ENDPOINT_URL']
# Sentry Config
SENTRY_DSN = env('SENTRY_DSN')
SENTRY_SAMPLE_RATE = env('SENTRY_SAMPLE_RATE')
RISK_ENVIRONMENT = env('RISK_ENVIRONMENT')
RISK_API_FQDN = env('RISK_API_FQDN')

SENTRY_CONFIG = {
    'dsn': SENTRY_DSN,
    'send_default_pii': True,
    'traces_sample_rate': SENTRY_SAMPLE_RATE,
    'release': sentry.fetch_git_sha(BASE_DIR),
    'environment': RISK_ENVIRONMENT,
    'debug': DEBUG,
    'tags': {
        'site': RISK_API_FQDN,
    },
}
if SENTRY_DSN:
    sentry.init_sentry(
        app_type='API',
        **SENTRY_CONFIG,
    )

SPECTACULAR_SETTINGS = {
    'TITLE': 'IFRC-GO RISK API',
    'DESCRIPTION': 'IFRC-GO RISK API Documenation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}
