from __future__ import absolute_import, unicode_literals

import os

import celery
from celery.signals import setup_logging
from django.conf import settings

from risk_module.sentry import init_sentry


class Celery(celery.Celery):
    def on_configure(self):
        if settings.SENTRY_DSN:
            init_sentry(app_type="WORKER", **settings.SENTRY_CONFIG)


@setup_logging.connect
def config_loggers(*args, **kwags):
    from logging.config import dictConfig

    from django.conf import settings

    dictConfig(settings.LOGGING)


# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "risk_module.settings")
app = Celery("risk_module")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
