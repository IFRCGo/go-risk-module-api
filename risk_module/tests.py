from django.test import TestCase


class FakeTest(TestCase):
    """
    This test is for running migrations only
    docker compose run --rm server ./manage.py test --keepdb -v 2 risk_module.tests.FakeTest
    """

    def test_fake(self):
        pass
