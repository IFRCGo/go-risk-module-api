import requests
import logging
import datetime
import os

from django.core.management.base import BaseCommand
from django.utils import timezone

from imminent.models import Pdc, PdcDisplacement
from common.models import HazardType, Country


logger = logging.getLogger()


class Command(BaseCommand):
    help = "Import Active Hazards"

    def parse_timestamp(self, timestamp):
        # NOTE: all timestamp are in millisecond and with timezone `utc`
        return timezone.make_aware(datetime.datetime.utcfromtimestamp(int(timestamp) / 1000))

    def parse_severity(self, severity):
        if severity == "WARNING":
            severity = Pdc.Severity.WARNING
        elif severity == "WATCH":
            severity = Pdc.Severity.WATCH
        elif severity == "ADVISORY":
            severity = Pdc.Severity.ADVISORY
        elif severity == "INFORMATION":
            severity = Pdc.Severity.INFORMATION
        return severity

    def handle(self, *args, **options):
        # NOTE: Use the search hazard api for the information download
        # make sure to use filter the data
        access_token = os.environ.get("PDC_ACCESS_TOKEN")
        url = "https://sentry.pdc.org/hp_srv/services/hazards/t/json/search_hazard"
        headers = {"Authorization": "Bearer {}".format(access_token)}
        # make sure to use the datetime now and timestamp for the post data
        # current date and time
        now = datetime.datetime.now()
        today_timestmap = str(datetime.datetime.timestamp(now)).replace(".", "")
        data = {
            "pagination": {"page": 1, "pagesize": 100},
            "order": {"orderlist": {"updateDate": "DESC"}},
            "restrictions": [[{"searchType": "LESS_THAN", "updateDate": today_timestmap}]],
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            error_log = f"Error querying PDC data at {url}"
            logger.error(error_log)
            logger.error(response.content)
        response_data = response.json()
        for data in response_data:
            # NOTE: Filter the active hazard only
            # Update the hazard if it has expired
            hazard_type = data["type_ID"]
            hazard_status = data["status"]
            if hazard_status == "E":
                pdcs = Pdc.objects.filter(uuid=data["uuid"])
                for pdc in pdcs:
                    pdc.status = Pdc.Status.EXPIRED
                    pdc.save(update_fields=["status"])
            if hazard_status == "A":
                if hazard_type == "WILDFIRE":
                    hazard_type = HazardType.WILDFIRE
                    pdc_updated_at = self.parse_timestamp(data["last_Update"])
                    if Pdc.objects.filter(
                        uuid=data["uuid"], hazard_type=hazard_type, pdc_updated_at=pdc_updated_at
                    ).exists():
                        continue
                    else:
                        data = {
                            "hazard_id": data["hazard_ID"],
                            "hazard_name": data["hazard_Name"],
                            "latitude": data["latitude"],
                            "longitude": data["longitude"],
                            "description": data["description"],
                            "hazard_type": hazard_type,
                            "uuid": data["uuid"],
                            "start_date": self.parse_timestamp(data["start_Date"]),
                            "end_date": self.parse_timestamp(data["end_Date"]),
                            "status": Pdc.Status.ACTIVE,
                            "pdc_created_at": self.parse_timestamp(data["create_Date"]),
                            "pdc_updated_at": self.parse_timestamp(data["last_Update"]),
                            "severity": self.parse_severity(data["severity_ID"]),
                        }
                        Pdc.objects.get_or_create(**data)

            # create pdc_displacement
            uuids = Pdc.objects.filter(status=Pdc.Status.ACTIVE, hazard_type=HazardType.WILDFIRE).values_list(
                "uuid", "hazard_type", "pdc_updated_at"
            )
            for uuid, hazard_type, pdc_updated_at in uuids:
                access_token = os.environ.get("PDC_ACCESS_TOKEN")
                url = f"https://sentry.pdc.org/hp_srv/services/hazard/{uuid}/exposure/latest/"
                headers = {"Authorization": "Bearer {}".format(access_token)}
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    error_log = f"Error querying PDC Exposure data at {url}"
                    logger.error(error_log)
                    logger.error(response.content)
                response_data = response.json()
                if PdcDisplacement.objects.filter(
                    pdc__uuid=uuid, pdc__hazard_type=hazard_type, pdc__pdc_updated_at=pdc_updated_at
                ).exists():
                    continue
                else:
                    for pdc in Pdc.objects.filter(uuid=uuid):
                        data = response_data.get("totalByCountry")
                        if data and len(data) > 0:
                            for d in data:
                                if Country.objects.filter(iso3=d["country"].lower()).exists():
                                    c_data = {
                                        "country": Country.objects.filter(iso3=d["country"].lower()).first(),
                                        "hazard_type": hazard_type,
                                        "population_exposure": d["population"],
                                        "capital_exposure": d["capital"],
                                        "pdc": pdc,
                                    }
                                    PdcDisplacement.objects.create(**c_data)
                        else:
                            PdcDisplacement.objects.create(hazard_type=hazard_type, pdc=pdc)

            # wildfire polygon
            uuids = Pdc.objects.filter(status=Pdc.Status.ACTIVE, hazard_type=HazardType.WILDFIRE).values_list(
                "uuid", flat=True
            )
            username = os.environ.get("PDC_USERNAME")
            password = os.environ.get("PDC_PASSWORD")
            for uuid in uuids:
                session = requests.Session()
                login_url = "https://partners.pdc.org/arcgis/tokens/generateToken"

                data = {
                    "f": "json",
                    "username": username,
                    "password": password,
                    "referer": "https://www.arcgis.com",
                }

                login_response = session.post(login_url, data=data, allow_redirects=True)
                access_token = login_response.json()["token"]

                session.headers.update(
                    {
                        "Authorization": f"Bearer {access_token}",
                    }
                )
                arch_gis_url = f"https://partners.pdc.org/arcgis/rest/services/partners/pdc_hazard_exposure/MapServer/27/query?where=hazard_uuid%3D%27{uuid}%27&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=&having=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentOnly=false&datumTransformation=&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson"
                arch_response = session.get(url=arch_gis_url)
                response_data = arch_response.json()
                for data in response_data["features"]:
                    features = data
                    for pdc in Pdc.objects.filter(uuid=uuid):
                        pdc.footprint_geojson = features
                        pdc.save(update_fields=["footprint_geojson"])
