import logging
import requests
import datetime
import typing

from django.core.management.base import BaseCommand
from django.conf import settings
from sentry_sdk.crons import monitor

from risk_module.sentry import SentryMonitor
from imminent.models import Pdc


logger = logging.getLogger(__name__)

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


def chunk_list(lst: typing.List[typing.Any], n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class Command(BaseCommand):
    help = "Import polygon from `uuid` from pdc arch-gis"

    @staticmethod
    def get_access_token(session: requests.Session) -> typing.Tuple[str, datetime.datetime]:
        login_url = "https://partners.pdc.org/arcgis/tokens/generateToken"

        data = {
            "f": "json",
            "username": settings.PDC_USERNAME,
            "password": settings.PDC_PASSWORD,
            "referer": "https://www.arcgis.com",
        }

        login_response = session.post(login_url, data=data, allow_redirects=True).json()
        return (
            login_response["token"],
            datetime.datetime.fromtimestamp(login_response["expires"]/1000),
        )

    @staticmethod
    def get_hazard_uuid_where_statement(uuid_list: typing.List[str]):
        """
        Returns:
            hazard_uuid IN ('uuid1', 'uuid2')
        """
        if len(uuid_list) == 0:
            return f"hazard_uuid = '{uuid_list[0]}'"

        list_value = (
            ",".join([
                f"'{_uuid}'" for _uuid in uuid_list
            ])
        )
        return f"hazard_uuid IN ({list_value})"

    def save_pdc_using_uuid(self, session, token_expires, uuid_list: typing.List[str]) -> bool:
        """
        Query PDC data from Arc GIS: https://partners.pdc.org/arcgis/rest/services/partners/pdc_hazard_exposure/MapServer/27/query
        """
        if token_expires is None or datetime.datetime.now() >= token_expires:
            access_token, token_expires = self.get_access_token(session)
            session.headers.update(
                {
                    "Authorization": f"Bearer {access_token}",
                }
            )

        # Fetch data for multiple uuids
        arc_gis_url = "https://partners.pdc.org/arcgis/rest/services/partners/pdc_hazard_exposure/MapServer/27/query"
        arc_response = session.post(
            url=arc_gis_url,
            data={
                **ARC_GIS_DEFAULT_PARAMS,
                # NOTE: Each new request has 6s+ response time, using where in query we reduce that latency
                "where": self.get_hazard_uuid_where_statement(uuid_list),
                "outFields": "hazard_uuid,type_id",
            },
        )

        # Save data for multiple uuids
        response_data = arc_response.json()

        if "features" not in response_data:
            # Sample error response: {'error': {'code': 400, 'message': 'Failed to execute query.', 'details': []}}
            if "error" in response_data:
                return False

        for feature in response_data["features"]:
            # XXX: Multiple row has same uuid
            _uuid = feature["properties"].pop("hazard_uuid")
            Pdc.objects.filter(uuid=_uuid).update(
                footprint_geojson=feature,
            )
        return True

    @monitor(monitor_slug=SentryMonitor.CREATE_PDC_POLYGON)
    def handle(self, *args, **kwargs):
        """
        Query PDC data from Arc GIS: https://partners.pdc.org/arcgis/rest/services/partners/pdc_hazard_exposure/MapServer/27/query
        """
        uuid_list = list(Pdc.objects.filter(status=Pdc.Status.ACTIVE).values_list("uuid", flat=True).distinct())
        retry_uuid_list = []
        session = requests.Session()
        token_expires = None
        for uuid_chunk_list in chunk_list(uuid_list, 5):
            if not self.save_pdc_using_uuid(session, token_expires, uuid_chunk_list):
                logger.warning(f'Failed to process uuids: {uuid_chunk_list}. Will try again individually')
                retry_uuid_list.extend(uuid_chunk_list)

        # For failed, try one by one again
        if retry_uuid_list:
            logger.info(f'Retrying {len(retry_uuid_list)} uuids')
            for uuid in retry_uuid_list:
                self.save_pdc_using_uuid(session, token_expires, [uuid])
