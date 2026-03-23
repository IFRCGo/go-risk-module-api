import signal
import time
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
from redis.exceptions import ConnectionError as RedisConnectionError


class TimeoutException(Exception): ...


class RetryHelper:
    def __init__(self, base_wait_seconds: int = 2, wait_max_seconds: int = 60):
        self.base_wait_seconds = base_wait_seconds
        self.wait_max_seconds = wait_max_seconds
        self.attempt = 1
        self.next_wait = base_wait_seconds
        self.start_time = time.time()

    def next_wait_seconds(self) -> int:
        return self.next_wait

    def wait(self) -> None:
        time.sleep(self.next_wait)
        self.attempt += 1
        if self.next_wait < self.wait_max_seconds:
            self.next_wait = self.base_wait_seconds**self.attempt
        else:
            self.next_wait = self.wait_max_seconds

    def total_time(self) -> float:
        return time.time() - self.start_time

    def try_again_message(self, prefix: str) -> str:
        return f"{prefix}, Attempt: {self.attempt}, try again after {self.next_wait_seconds()} seconds..."


def timeout_handler(*_):
    raise Exception("The command timed out.")


class Command(BaseCommand):
    help = "Wait for resources our application depends on"

    def wait_for_db(self):
        self.stdout.write("Waiting for DB...")
        db_conn = None
        retry_helper = RetryHelper()
        while True:
            try:
                db_conn = connections["default"]
                db_conn.ensure_connection()
                break
            except OperationalError:
                ...
            # Try again
            self.stdout.write(self.style.WARNING(retry_helper.try_again_message("DB not available")))
            retry_helper.wait()

        self.stdout.write(self.style.SUCCESS(f"DB is available after {retry_helper.total_time()} seconds"))

    def wait_for_redis(self):
        self.stdout.write("Waiting for Redis...")
        redis_conn = None
        retry_helper = RetryHelper()
        while True:
            try:
                cache.set("wait-for-it-ping", "pong", timeout=1)  # Set a key to check Redis availability
                redis_conn = cache.get("wait-for-it-ping")  # Try to get the value back from Redis
                if redis_conn != "pong":
                    raise TypeError
                break
            except (RedisConnectionError, TypeError):
                ...
            # Try again
            self.stdout.write(self.style.WARNING(retry_helper.try_again_message("Redis not available")))
            retry_helper.wait()

        self.stdout.write(self.style.SUCCESS(f"Redis is available after {retry_helper.total_time()} seconds"))

    def wait_for_minio(self):
        self.stdout.write("Waiting for Minio...")
        endpoint_url = getattr(settings, "AWS_S3_PROXIES", {}).get("http") or getattr(settings, "AWS_S3_ENDPOINT_URL", None)
        if endpoint_url is None:
            self.stdout.write(self.style.WARNING("No endpoint_url is provided. Skipping wait"))
            return

        retry_helper = RetryHelper()
        while True:
            try:
                response = requests.get(urljoin(endpoint_url, "/minio/health/live"), timeout=5)
                if response.status_code == 200:
                    break
            except requests.exceptions.RequestException:
                ...
            # Try again
            self.stdout.write(self.style.WARNING(retry_helper.try_again_message("Minio not available")))
            retry_helper.wait()

        self.stdout.write(self.style.SUCCESS(f"Minio is available after {retry_helper.total_time()} seconds"))

    def add_arguments(self, parser):
        parser.add_argument(
            "--timeout",
            type=int,
            default=600,
            help="The maximum time (in seconds) the command is allowed to run before timing out. Default is 10 min.",
        )
        parser.add_argument("--db", action="store_true", help="Wait for DB to be available")
        parser.add_argument("--redis", action="store_true", help="Wait for Redis to be available")
        parser.add_argument("--minio", action="store_true", help="Wait for MinIO (S3) storage to be available")
        parser.add_argument("--all", action="store_true", help="Wait for all to be available")

    def handle(self, **kwargs):
        timeout = kwargs["timeout"]
        _all = kwargs["all"]

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)

        try:
            if _all or kwargs["db"]:
                self.wait_for_db()
            if _all or kwargs["minio"]:
                self.wait_for_minio()
            if _all or kwargs["redis"]:
                self.wait_for_redis()
        except TimeoutException:
            ...
        finally:
            # Disable the alarm (cleanup)
            signal.alarm(0)
