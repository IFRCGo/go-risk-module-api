from __future__ import absolute_import
import os
import celery
from django.conf import settings
from risk_module.sentry import init_sentry


class Celery(celery.Celery):
    def on_configure(self):
        if settings.SENTRY_DSN:
            init_sentry(app_type="WORKER", **settings.SENTRY_CONFIG)


# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "risk_module.settings")
app = Celery("risk_module")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
