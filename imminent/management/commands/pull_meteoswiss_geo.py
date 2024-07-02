import boto3
import logging
import json
import os
from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings
from imminent.models import MeteoSwiss
from common.models import Country

logger = logging.getLogger(__name__)


# TODO: This is not approved to be used in production
# This is run in staging only for now
class Command(BaseCommand):
    help = "Import Meteoswiss Data"

    def parse_date(self, date):
        return datetime.strptime(date, "%Y%m%d%H")

    def import_meteoswiss_data(self, s3):
        bucket = s3.Bucket(settings.METEO_SWISS_S3_BUCKET)

        for obj in bucket.objects.all():
            path, filename = os.path.split(obj.key)

            if filename.endswith(".geojson"):
                self.import_geojson_data(obj, path, filename)

    def import_geojson_data(self, obj, path, filename):
        filename_splitted = filename.split("_")
        country_name = filename_splitted[4]
        impact_type = "_".join(filename_splitted[5:8])
        country = Country.objects.filter(name=country_name).first()
        initialization_date = self.parse_date(filename_splitted[2].replace('run', ''))
        if country:
            meteoswiss = MeteoSwiss.objects.filter(
                impact_type=impact_type,
                folder_id=path,
                country=country,
                initialization_date=initialization_date
            ).first()

            if meteoswiss:
                details = obj.get()["Body"].read().decode("utf-8")
                json_details = json.loads(details)
                meteoswiss.footprint_geojson = json_details
                meteoswiss.save(update_fields=['footprint_geojson'])

    def handle(self, *args, **kwargs):
        session = boto3.session.Session()

        s3 = session.resource(
            service_name="s3",
            endpoint_url=settings.METEO_SWISS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.METEO_SWISS_S3_ACCESS_KEY,
            aws_secret_access_key=settings.METEO_SWISS_S3_SECRET_KEY,
        )

        self.import_meteoswiss_data(s3)
