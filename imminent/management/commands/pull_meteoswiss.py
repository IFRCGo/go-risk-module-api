import boto3
import logging
import json
import os
from datetime import datetime

from django.core.management.base import BaseCommand
from imminent.models import MeteoSwiss
from common.models import Country, HazardType

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import Meteoswiss Data"

    def parse_date(self, date):
        return datetime.strptime(date, "%Y%m%d%H")

    def handle(self, *args, **kwargs):
        session = boto3.session.Session()

        s3 = session.resource(
            service_name="s3",
            aws_access_key_id="ifrc_hydrometimpactoutlookproduct",
            aws_secret_access_key="pwd4hydroimpactdepl",
            endpoint_url="https://servicedepl.meteoswiss.ch",
        )

        bucket = s3.Bucket("ch.meteoswiss.hydrometimpact.outlook-product")
        for obj in bucket.objects.all():
            # split the folder here
            path, filename = os.path.split(obj.key)
            # check if the path already exists and
            # if not only pull the data
            # lets store the path here to check for the data to pull
            if filename.endswith(".json"):
                filename_splitted = filename.split("_")
                country_name = filename_splitted[4]
                # get country from filename
                details = obj.get()["Body"].read().decode("utf-8")
                json_details = json.loads(details)
                data = {
                    "country": Country.objects.filter(name=country_name).first(),
                    "event_details": json_details,
                    "hazard_name": json_details["eventName"],
                    "folder_id": path,
                    "initialization_date": self.parse_date(json_details["initializationTime"]),
                    "event_date": self.parse_date(json_details["eventDate"]),
                    "impact_type": json_details["impactType"],
                    "hazard_type": HazardType.CYCLONE,
                }
                MeteoSwiss.objects.get_or_create(**data)
        for obj in bucket.objects.all():
            # split the folder here
            # folder is determined from path
            path, filename = os.path.split(obj.key)
            if filename.endswith(".geojson"):
                details = obj.get()["Body"].read().decode("utf-8")
                filename_splitted = filename.split("_")
                country_name = filename_splitted[4]
                impact_type = filename_splitted[5] + "_" + filename_splitted[6] + "_" + filename_splitted[7]
                meteoswiss = MeteoSwiss.objects.filter(
                    impact_type=impact_type, folder_id=path, country=Country.objects.filter(name=country_name).first()
                )
                json_details = json.loads(details)
                if meteoswiss.exists():
                    meteoswiss = meteoswiss.first()
                    meteoswiss.footprint_geojson = json_details
                    meteoswiss.save()
