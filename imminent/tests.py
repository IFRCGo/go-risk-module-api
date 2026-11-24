from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from imminent.models import Oddrin


class OddrinViewSetTest(TestCase):
    list_url = "/api/v1/global-exposure-data/"

    def setUp(self):
        self.client = APIClient()
        self.oddrin = Oddrin.objects.create(hazard_title="Test hazard")
        self.detail_url = f"{self.list_url}{self.oddrin.pk}/"

    def _write_requests(self):
        return [
            ("post", self.list_url),
            ("put", self.detail_url),
            ("patch", self.detail_url),
            ("delete", self.detail_url),
        ]

    def test_anonymous_can_read(self):
        assert self.client.get(self.list_url).status_code == status.HTTP_200_OK
        assert self.client.get(self.detail_url).status_code == status.HTTP_200_OK

    def test_anonymous_cannot_write(self):
        for method, url in self._write_requests():
            resp = getattr(self.client, method)(url, {"hazard_title": "Changed"}, format="json")
            assert resp.status_code == status.HTTP_403_FORBIDDEN, (method, resp.status_code)
        self.oddrin.refresh_from_db()
        assert self.oddrin.hazard_title == "Test hazard"

    def test_authenticated_write_is_not_allowed(self):
        user = get_user_model().objects.create_user(username="user", password="password")
        self.client.force_authenticate(user)
        for method, url in self._write_requests():
            resp = getattr(self.client, method)(url, {"hazard_title": "Changed"}, format="json")
            assert resp.status_code == status.HTTP_405_METHOD_NOT_ALLOWED, (method, resp.status_code)
        self.oddrin.refresh_from_db()
        assert self.oddrin.hazard_title == "Test hazard"
        assert Oddrin.objects.count() == 1
