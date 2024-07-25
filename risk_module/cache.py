import time
from contextlib import contextmanager

from django.conf import settings
from django.core.cache import caches
from django_redis.client import DefaultClient

from risk_module.sentry import SentryMonitor

cache: DefaultClient = caches["default"]


class CacheKey:
    class RedisLockKey:
        _BASE = "dj-lock-"

    @classmethod
    def get_sm_lock(cls, enum: SentryMonitor) -> str:
        """
        Return SentryMonitor lock key used by cron tasks
        """
        return f"{cls.RedisLockKey._BASE}-SM-{enum.name}"


@contextmanager
def redis_lock(
    lock_id: str,
    lock_expire: int = settings.REDIS_DEFAULT_LOCK_EXPIRE,
):
    timeout_at = time.monotonic() + lock_expire - 3
    # cache.add fails if the key already exists
    status = cache.add(lock_id, 1, lock_expire)
    try:
        yield status
    finally:
        # memcache delete is very slow, but we have to use it to take
        # advantage of using add() for atomic locking
        if time.monotonic() < timeout_at and status:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else
            # also don't release the lock if we didn't acquire it
            cache.delete(lock_id)
