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
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-6=h&-fnse4%ul(sxri7zgkscx$0r58wro(3m)-trw558!$bwen'
)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [os.environ.get('DJANGO_ALLOWED_HOST', 'localhost')]


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
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50,
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
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'PORT': os.environ['DATABASE_PORT'],
        'HOST': os.environ['DATABASE_HOST'],
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

TIME_ZONE = os.environ.get('TIME_ZONE', 'UTC')

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


if os.environ.get('USE_AWS_FOR_MEDIA', 'false').lower() == 'true':
    AWS_S3_ACCESS_KEY_ID = os.environ['S3_AWS_ACCESS_KEY_ID']
    AWS_S3_SECRET_ACCESS_KEY = os.environ['S3_AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['S3_STORAGE_BUCKET_NAME']
    AWS_S3_REGION_NAME = os.environ['S3_REGION_NAME']

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


CELERY_REDIS_URL = os.environ.get('CELERY_REDIS_URL', 'redis://redis:6379/0')
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
    "check_pdc_status": {
        "task": "imminent.tasks.check_pdc_status",
        "schedule": crontab(minute=0, hour=1)  # This task to execute daily in 1 AM(UTC)
    },
    "create_hazard_information": {
        "task": "seasonal.tasks.import_think_hazard_informations",
        "schedule": crontab(0, 0, day_of_month='2')  # This task execute at second day of every month
    }
}

CORS_ORIGIN_ALLOW_ALL = True
