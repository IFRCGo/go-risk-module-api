import datetime
import logging
import typing

import requests
from django.conf import settings
from django.db import models

from common.models import HazardType
from imminent.models import Pdc

from .utils import chunk_list, parse_timestamp

logger = logging.getLogger(__name__)


class SentryPdcSource:
    class URL:
        # NOTE: Make sure to use filter while using SENTRY_PDC_SEARCH_HAZARD
        PDC_SEARCH_HAZARD = "https://sentry.pdc.org/hp_srv/services/hazards/t/json/search_hazard"
        PDC_ACTIVE_HAZARD = "https://sentry.pdc.org/hp_srv/services/hazards/t/json/get_active_hazards"

        @staticmethod
        def get_hazard_exposure_latest(uuid: str) -> str:
            return f"https://sentry.pdc.org/hp_srv/services/hazard/{uuid}/exposure/latest/"

    SEVERITY_MAP: typing.Dict[str, Pdc.Severity] = {
        "WARNING": Pdc.Severity.WARNING,
        "WATCH": Pdc.Severity.WATCH,
        "ADVISORY": Pdc.Severity.ADVISORY,
        "INFORMATION": Pdc.Severity.INFORMATION,
    }

    HAZARD_TYPE_MAP: typing.Dict[str, HazardType] = {
        "FLOOD": HazardType.FLOOD,
        "CYCLONE": HazardType.CYCLONE,
        "STORM": HazardType.STORM,
        "DROUGHT": HazardType.DROUGHT,
        "WIND": HazardType.WIND,
        "TSUNAMI": HazardType.TSUNAMI,
        "EARTHQUAKE": HazardType.EARTHQUAKE,
        "WILDFIRE": HazardType.WILDFIRE,
    }

    class dcSaveData(typing.NamedTuple):
        hazard_id: str
        hazard_name: str
        hazard_type: typing.Optional[HazardType]
        latitude: float
        longitude: float
        description: str
        start_date: str  # datetime.date
        end_date: str  # datetime.date
        pdc_created_at: str  # datetime.datetime
        pdc_updated_at: str  # datetime.datetime
        severity: typing.Optional[str]

    @staticmethod
    def authorization_headers():
        return {"Authorization": "Bearer {}".format(settings.PDC_ACCESS_TOKEN)}

    @classmethod
    def parse_response_data(cls, data: dict) -> dcSaveData:
        return cls.dcSaveData(
            hazard_id=data["hazard_ID"],
            hazard_name=data["hazard_Name"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            description=data["description"],
            hazard_type=data["type_ID"],
            severity=data["severity_ID"],
            start_date=data["start_Date"],
            end_date=data["end_Date"],
            pdc_created_at=data["create_Date"],
            pdc_updated_at=data["last_Update"],
        )

    @classmethod
    def save_pdc_data(cls, uuid: str, data: dcSaveData):
        # Parse Hazard Type
        if data.hazard_type is None:
            return
        hazard_type = cls.HAZARD_TYPE_MAP.get(data.hazard_type.upper())
        if hazard_type is None:
            return

        pdc_updated_at = parse_timestamp(data.pdc_updated_at)

        # NOTE: Check if we have up to date data already
        existing_qs = Pdc.objects.filter(
            uuid=uuid,
            pdc_updated_at=pdc_updated_at,
        )
        if existing_qs.exists():
            return

        # Data transform
        pdc_data = {
            **data._asdict(),
            "status": Pdc.Status.ACTIVE,
            "hazard_type": hazard_type,
            "start_date": parse_timestamp(data.start_date),
            "end_date": parse_timestamp(data.end_date),
            "pdc_created_at": parse_timestamp(data.pdc_created_at),
            "pdc_updated_at": pdc_updated_at,
            "severity": (data.severity and cls.SEVERITY_MAP.get(data.severity.upper())),
            "stale_displacement": True,  # NOTE: Another cron job will update this data
        }
        # Create or update existing data
        Pdc.objects.update_or_create(uuid=uuid, defaults=pdc_data)


class ArcGisPdcSource:
    # Check https://partners.pdc.org/arcgis/rest/services/partners/pdc_hazard_exposure/MapServer/27/query for fields/values
    ARC_GIS_DEFAULT_PARAMS = {
        # Required values
        "geometryType": "esriGeometryEnvelope",
        "spatialRel": "esriSpatialRelIntersects",
        "returnGeometry": True,
        "returnTrueCurves": False,
        "returnIdsOnly": False,
        "returnCountOnly": False,
        "returnZ": False,
        "returnM": False,
        "returnDistinctValues": False,
        "returnExtentOnly": False,
        "featureEncoding": "esriDefault",
        "f": "geojson",
        # Empty values
        "text": "",
        "objectIds": "",
        "time": "",
        "geometry": "",
        "inSR": "",
        "relationParam": "",
        "outFields": "",
        "maxAllowableOffset": "",
        "geometryPrecision": "",
        "outSR": "",
        "having": "",
        "orderByFields": "",
        "groupByFieldsForStatistics": "",
        "outStatistics": "",
        "gdbVersion": "",
        "historicMoment": "",
        "resultOffset": "",
        "resultRecordCount": "",
        "queryByDistance": "",
        "datumTransformation": "",
        "parameterValues": "",
        "rangeValues": "",
        "quantizationParameters": "",
    }

    class AccessTokenManager:
        def __init__(self, session: requests.Session):
            self.token_expires = None
            self.token_expires = None
            self.session = session

        def get_access_token(self):
            login_url = "https://partners.pdc.org/arcgis/tokens/generateToken"

            data = {
                "f": "json",
                "username": settings.PDC_USERNAME,
                "password": settings.PDC_PASSWORD,
                "referer": "https://www.arcgis.com",
            }

            login_response = self.session.post(login_url, data=data, allow_redirects=True).json()
            return (
                login_response["token"],
                datetime.datetime.fromtimestamp(login_response["expires"] / 1000),
            )

        def update(self):
            if self.token_expires is None or datetime.datetime.now() >= self.token_expires:
                self.access_token, self.token_expires = self.get_access_token()
                self.session.headers.update(
                    {
                        "Authorization": f"Bearer {self.access_token}",
                    }
                )

    class CommandMixin:
        chunk_size = 5

        @staticmethod
        def generate_uuid_where_statement(field: str, uuid_list: typing.List[str]):
            """
            Returns:
                eg: hazard_uuid IN ('uuid1', 'uuid2')
            """
            if len(uuid_list) == 0:
                return f"{field} = '{uuid_list[0]}'"

            list_value = ",".join([f"'{_uuid}'" for _uuid in uuid_list])
            return f"{field} IN ({list_value})"

        @staticmethod
        def is_valid_arc_response(data):
            if "features" not in data:
                # Sample error response:
                #  {'error': {'code': 400, 'message': 'Failed to execute query.', 'details': []}}
                if "error" in data:
                    return False
            return True

        def save_pdc_using_uuid(self, session: requests.Session, uuid_list: typing.List[str]) -> bool:
            """
            Query and save pdc polygon data from Arc GIS for given uuids
            """
            raise NotImplementedError()

        def get_pdc_queryset(self) -> models.QuerySet[Pdc]:
            return Pdc.objects.filter(status=Pdc.Status.ACTIVE)

        def process(self):
            """List active uuids and pass it to save_pdc_using_uuid in chunk"""
            uuid_list = list(self.get_pdc_queryset().values_list("uuid", flat=True).distinct())

            retry_uuid_list = []
            session = requests.Session()
            token_manager = ArcGisPdcSource.AccessTokenManager(session)

            for uuid_chunk_list in chunk_list(uuid_list, self.chunk_size):
                token_manager.update()
                if not self.save_pdc_using_uuid(session, uuid_chunk_list):
                    logger.warning(f"Failed to process uuids: {uuid_chunk_list}. Will try again individually")
                    retry_uuid_list.extend(uuid_chunk_list)

            # For failed, try one by one again
            if retry_uuid_list:
                logger.info(f"Retrying {len(retry_uuid_list)} uuids")
                for uuid in retry_uuid_list:
                    token_manager.update()
                    self.save_pdc_using_uuid(session, [uuid])
