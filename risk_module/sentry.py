import os
import typing

import sentry_sdk
from difflib import context_diff
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.db import models
from celery.exceptions import Retry as CeleryRetry
from celery.schedules import crontab
from sentry_sdk.integrations.logging import ignore_logger
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# Celery Terminated Exception: The worker processing a job has been terminated by user request.
from billiard.exceptions import Terminated

IGNORED_ERRORS = [
    Terminated,
    PermissionDenied,
    CeleryRetry,
]
IGNORED_LOGGERS = [
    'django.core.exceptions.ObjectDoesNotExist',
]

for _logger in IGNORED_LOGGERS:
    ignore_logger(_logger)


class InvalidGitRepository(Exception):
    pass


def fetch_git_sha(path, head=None):
    """
    Source: https://github.com/getsentry/raven-python/blob/03559bb05fd963e2be96372ae89fb0bce751d26d/raven/versioning.py
    >>> fetch_git_sha(os.path.dirname(__file__))
    """
    if not head:
        head_path = os.path.join(path, '.git', 'HEAD')
        if not os.path.exists(head_path):
            raise InvalidGitRepository(
                'Cannot identify HEAD for git repository at %s' % (path,))

        with open(head_path, 'r') as fp:
            head = str(fp.read()).strip()

        if head.startswith('ref: '):
            head = head[5:]
            revision_file = os.path.join(
                path, '.git', *head.split('/')
            )
        else:
            return head
    else:
        revision_file = os.path.join(path, '.git', 'refs', 'heads', head)

    if not os.path.exists(revision_file):
        if not os.path.exists(os.path.join(path, '.git')):
            raise InvalidGitRepository(
                '%s does not seem to be the root of a git repository' % (path,))

        # Check for our .git/packed-refs' file since a `git gc` may have run
        # https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery
        packed_file = os.path.join(path, '.git', 'packed-refs')
        if os.path.exists(packed_file):
            with open(packed_file) as fh:
                for line in fh:
                    line = line.rstrip()
                    if line and line[:1] not in ('#', '^'):
                        try:
                            revision, ref = line.split(' ', 1)
                        except ValueError:
                            continue
                        if ref == head:
                            return str(revision)

        raise InvalidGitRepository(
            'Unable to find ref to head "%s" in repository' % (head,))

    with open(revision_file) as fh:
        return str(fh.read()).strip()


def init_sentry(app_type, tags={}, **config):
    integrations = [
        CeleryIntegration(),
        DjangoIntegration(),
        RedisIntegration(),
    ]
    sentry_sdk.init(
        **config,
        ignore_errors=IGNORED_ERRORS,
        integrations=integrations,
    )
    with sentry_sdk.configure_scope() as scope:
        scope.set_tag('app_type', app_type)
        for tag, value in tags.items():
            scope.set_tag(tag, value)


class SentryMonitor(models.TextChoices):
    """
    This class is used to create Sentry monitor of cron jobs
    """

    IMPORT_EARTHQUAKE_DATA = "import_earthquake_data", "0 0 * * *"
    CREATE_PDC_DATA = "create_pdc_data", "0 */2 * * *"
    CREATE_PDC_DAILY = "create_pdc_daily", "0 5 * * *"
    CREATE_PDC_DISPLACEMENT = "create_pdc_displacement", "0 */3 * * *"
    CREATE_PDC_POLYGON = "create_pdc_polygon", "0 */6 * * *"
    CREATE_PDC_INTENSITY = "create_pdc_intensity", "0 */7 * * *"
    CHECK_PDC_STATUS = "check_pdc_status", "0 1 * * *"
    CREATE_HAZARD_INFORMATION = "create_hazard_information", "0 0 2 * *"
    CREATE_ADAM_EXPOSURE = "create_adam_exposure", "0 */4 * * *"
    UPDATE_ADAM_CYCLONE = "update_adam_cyclone", "0 */4 * * *"
    IMPORT_GDACS_DATA = "import_gdacs_data", "0 */4 * * *"
    PULL_METEOSWISS = "pull_meteoswiss", "0 */4 * * *"
    PULL_METEOSWISS_GEO = "pull_meteoswiss_geo", "0 */4 * * *"
    METEOSWISS_AGG = "meteoswiss_agg", "0 */4 * * *"
    UPDATE_ADAM_ALERT_LEVEL = "update_adam_alert_level", "0 */4 * * *"

    @staticmethod
    def _crontab_to_string(c: crontab):
        return f"{c._orig_minute} {c._orig_hour} {c._orig_day_of_month} {c._orig_month_of_year} {c._orig_day_of_week}"

    @classmethod
    def load_cron_data(cls) -> typing.List[typing.Tuple[str, str]]:
        return [(key, cls._crontab_to_string(metadata["schedule"])) for key, metadata in settings.CELERY_BEAT_SCHEDULE.items()]

    @classmethod
    def validate_config(cls):
        """
        Validate SentryMonitor task list with Helm
        """
        current_helm_crons = cls.load_cron_data()
        assert set(cls.choices) == set(current_helm_crons), (
            # Show a simple diff for correction
            "SentryMonitor needs update\n\n"
            + (
                "\n".join(
                    list(
                        context_diff(
                            [f"{c} {s}" for c, s in set(cls.choices)],
                            [f"{c} {s}" for c, s in set(current_helm_crons)],
                            fromfile="SentryMonitor",
                            tofile="CELERY_BEAT_SCHEDULE",
                        )
                    )
                )
            )
        )
