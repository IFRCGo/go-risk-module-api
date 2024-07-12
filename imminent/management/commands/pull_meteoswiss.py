import boto3
import logging
import json
import os
import pytz
from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from sentry_sdk.crons import monitor

from risk_module.sentry import SentryMonitor
from imminent.models import MeteoSwiss
from common.models import Country, HazardType

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import Meteoswiss Data"

    def parse_date(self, date):
        date = datetime.strptime(date, "%Y%m%d%H")
        return date.replace(tzinfo=pytz.UTC)

    def import_meteoswiss_data(self, s3):
        bucket = s3.Bucket(settings.METEO_SWISS_S3_BUCKET)

        for obj in bucket.objects.all():
            path, filename = os.path.split(obj.key)

            if filename.endswith(".json"):
                self.import_json_data(obj, path, filename)

    def import_json_data(self, obj, path, filename):
        filename_splitted = filename.split("_")
        country_name = filename_splitted[4]
        model_name = filename_splitted[1]
        country = Country.objects.filter(
            name=country_name,
            record_type=Country.CountryType.COUNTRY
        ).first()

        if country:
            details = obj.get()["Body"].read().decode("utf-8")
            json_details = json.loads(details)
            impact_type = json_details["impactType"]
            data = {
                "country": country,
                "event_details": json_details,
                "hazard_name": json_details["eventName"],
                "folder_id": path,
                "initialization_date": self.parse_date(json_details["initializationTime"]),
                "event_date": self.parse_date(json_details["eventDate"]),
                "impact_type": impact_type,
                "hazard_type": HazardType.CYCLONE,
                "model_name": model_name,
            }
            if not MeteoSwiss.objects.filter(country=country, folder_id=path, impact_type=impact_type).exists():
                MeteoSwiss.objects.create(
                    **data
                )

    @monitor(monitor_slug=SentryMonitor.PULL_METEOSWISS)
    def handle(self, *args, **kwargs):
        session = boto3.session.Session()

        s3 = session.resource(
            service_name="s3",
            endpoint_url=settings.METEO_SWISS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.METEO_SWISS_S3_ACCESS_KEY,
            aws_secret_access_key=settings.METEO_SWISS_S3_SECRET_KEY,
        )
        self.import_meteoswiss_data(s3)
