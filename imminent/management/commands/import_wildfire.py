import datetime
import logging

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from common.models import Country, HazardType
from common.utils import logging_response_context
from imminent.models import Pdc, PdcDisplacement
from imminent.sources.pdc import SentryPdcSource

logger = logging.getLogger(__name__)


# Deprecated: Not used
class Command(BaseCommand):
    help = "Import Active Hazards"

    def parse_timestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.utcfromtimestamp(int(timestamp) / 1000))

    def parse_severity(self, severity):
        severity_map = {
            "WARNING": Pdc.Severity.WARNING,
            "WATCH": Pdc.Severity.WATCH,
            "ADVISORY": Pdc.Severity.ADVISORY,
            "INFORMATION": Pdc.Severity.INFORMATION,
        }
        return severity_map.get(severity, severity)

    def fetch_data(self, url, data):
        headers = {"Authorization": f"Bearer {settings.PDC_ACCESS_TOKEN}"}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            logger.error(
                "Error querying PDC data",
                extra=logging_response_context(response),
            )
            # TODO: return None?

        return response.json()

    def fetch_exposure_data(self, uuid):
        url = f"https://sentry.pdc.org/hp_srv/services/hazard/{uuid}/exposure/latest/"
        headers = {"Authorization": f"Bearer {settings.PDC_ACCESS_TOKEN}"}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logger.error(
                "Error querying PDC Exposure data",
                extra=logging_response_context(response),
            )
            # TODO: return None?

        return response.json()

    def fetch_polygon_data(self, uuid):
        session = requests.Session()
        login_url = "https://partners.pdc.org/arcgis/tokens/generateToken"

        data = {
            "f": "json",
            "username": settings.PDC_USERNAME,
            "password": settings.PDC_PASSWORD,
            "referer": "https://www.arcgis.com",
        }

        login_response = session.post(login_url, data=data, allow_redirects=True)
        access_token = login_response.json()["token"]

        session.headers.update({"Authorization": f"Bearer {access_token}"})
        arch_gis_url = (
            f"https://partners.pdc.org/arcgis/rest/services/partners/pdc_hazard_exposure/MapServer/27/query"
            f"?where=hazard_uuid%3D%27{uuid}%27"
            f"&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects"
            f"&relationParam=&outFields=&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision="
            f"&outSR=&having=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics="
            f"&outStatistics=&returnZ=false&returnM=false&gdbVersion=&historicMoment=&returnDistinctValues=false"
            f"&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentOnly=false&datumTransformation="
            f"&parameterValues=&rangeValues=&quantizationParameters=&featureEncoding=esriDefault&f=geojson"
        )
        arch_response = session.get(url=arch_gis_url)
        return arch_response.json()

    def create_or_update_pdc(self, data):
        hazard_type = HazardType.WILDFIRE
        pdc_updated_at = self.parse_timestamp(data["last_Update"])
        pdc_uuid = data["uuid"]

        existing_qs = Pdc.objects.filter(
            uuid=pdc_uuid,
            hazard_type=hazard_type,
            pdc_updated_at=pdc_updated_at,
        )
        if existing_qs.exists():
            return

        pdc_data = {
            "hazard_id": data["hazard_ID"],
            "hazard_name": data["hazard_Name"],
            "latitude": data["latitude"],
            "longitude": data["longitude"],
            "description": data["description"],
            "hazard_type": hazard_type,
            "start_date": self.parse_timestamp(data["start_Date"]),
            "end_date": self.parse_timestamp(data["end_Date"]),
            "status": Pdc.Status.ACTIVE,
            "pdc_created_at": self.parse_timestamp(data["create_Date"]),
            "pdc_updated_at": self.parse_timestamp(data["last_Update"]),
            "severity": self.parse_severity(data["severity_ID"]),
        }
        Pdc.objects.update_or_create(uuid=pdc_uuid, defaults=pdc_data)

    def create_displacement_records(self, uuid, hazard_type, total_by_country):
        for pdc in Pdc.objects.filter(uuid=uuid):
            for d in total_by_country:
                iso3_country = d["country"].lower()
                if Country.objects.filter(iso3=iso3_country).exists():
                    country = Country.objects.filter(iso3=iso3_country).last()
                    c_data = {
                        "country": country,
                        "hazard_type": hazard_type,
                        "population_exposure": d["population"],
                        "capital_exposure": d["capital"],
                        "pdc": pdc,
                    }
                    PdcDisplacement.objects.create(**c_data)
            else:
                PdcDisplacement.objects.create(hazard_type=hazard_type, pdc=pdc)

    def update_pdc_footprint(self, uuid, footprint_geojson):
        return Pdc.objects.filter(uuid=uuid).update(footprint_geojson=footprint_geojson.get("features"))

    def handle(self, *args, **options):
        now = datetime.datetime.now()
        today_timestamp = str(int(datetime.datetime.timestamp(now) * 1000))
        data = {
            "pagination": {"page": 1, "pagesize": 100},
            "order": {"orderlist": {"updateDate": "DESC"}},
            "restrictions": [[{"searchType": "LESS_THAN", "updateDate": today_timestamp}]],
        }
        response_data = self.fetch_data(SentryPdcSource.URL.PDC_SEARCH_HAZARD, data)

        for data in response_data:
            hazard_status = data["status"]
            if hazard_status == "E":
                Pdc.objects.filter(uuid=data["uuid"]).filter(status=Pdc.Status.EXPIRED)

            elif hazard_status == "A":
                self.create_or_update_pdc(data)
                exposure_data = self.fetch_exposure_data(data["uuid"])
                hazard_type = HazardType.WILDFIRE
                pdc_updated_at = self.parse_timestamp(data["last_Update"])
                if not PdcDisplacement.objects.filter(
                    pdc__uuid=data["uuid"], pdc__hazard_type=hazard_type, pdc__pdc_updated_at=pdc_updated_at
                ).exists():
                    self.create_displacement_records(
                        data["uuid"],
                        hazard_type,
                        exposure_data.get("totalByCountry", []),
                    )
                polygon_data = self.fetch_polygon_data(data["uuid"])
                self.update_pdc_footprint(data["uuid"], polygon_data)
