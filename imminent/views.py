from datetime import datetime, timedelta

from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import response, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView

from common.models import HazardType
from imminent.filter_set import (
    AdamFilterSet,
    EarthquakeFilterSet,
    GDACSFilterSet,
    GWISFilterSet,
    MeteoSwissAggFilterSet,
    PdcFilterSet,
)
from imminent.models import (
    GDACS,
    GWIS,
    Adam,
    Earthquake,
    MeteoSwissAgg,
    Oddrin,
    Pdc,
    PdcDisplacement,
)
from imminent.serializers import (
    AdamExposureSerializer,
    AdamSerializer,
    CountryImminentRequestSerializer,
    CountryImminentSerializer,
    EarthquakeSerializer,
    GDACSExposureSerializer,
    GDACSSeralizer,
    GWISSerializer,
    MeteoSwissAggSerializer,
    MeteoSwissFootprintSerializer,
    OddrinSerializer,
    PdcDisplacementSerializer,
    PdcExposureSerializer,
    PdcSerializer,
)


class EarthquakeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Earthquake.objects.all()
    serializer_class = EarthquakeSerializer
    filterset_class = EarthquakeFilterSet


class OddrinViewSet(viewsets.ModelViewSet):
    queryset = Oddrin.objects.all()
    serializer_class = OddrinSerializer


class PdcDisplacementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PdcDisplacementSerializer

    def get_queryset(self):
        return PdcDisplacement.objects.filter(
            pdc__status=Pdc.Status.ACTIVE,
        ).select_related("country")


class ImminentViewSet(viewsets.ViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("iso3", "hazard_type")

    def list(self, request, *args, **kwargs):
        today = datetime.now().date()
        seven_days_before = today + timedelta(days=-7)
        three_days_before = today + timedelta(days=-3)
        iso3 = self.request.query_params.get("iso3")
        region = self.request.query_params.get("region")
        if iso3:
            oddrin_data = OddrinSerializer(Oddrin.objects.filter(iso3__icontains=iso3), many=True).data
            pdc_data = PdcDisplacementSerializer(
                PdcDisplacement.objects.filter(
                    models.Q(
                        country__iso3__icontains=iso3,
                        pdc__status=Pdc.Status.ACTIVE,
                        pdc__start_date__gte=seven_days_before,
                        pdc__hazard_type__in=[HazardType.FLOOD, HazardType.CYCLONE],
                    )
                    | models.Q(
                        country__iso3__icontains=iso3,
                        pdc__status=Pdc.Status.ACTIVE,
                        pdc__pdc_updated_at__isnull=True,
                        pdc__start_date__gte=seven_days_before,
                        pdc__hazard_type__in=[HazardType.FLOOD, HazardType.CYCLONE],
                    )
                    | models.Q(
                        country__iso3__icontains=iso3,
                        pdc__status=Pdc.Status.ACTIVE,
                        pdc__start_date__gte=three_days_before,
                        pdc__hazard_type=HazardType.EARTHQUAKE,
                    )
                    | models.Q(
                        country__iso3__icontains=iso3,
                        pdc__status=Pdc.Status.ACTIVE,
                        pdc__pdc_updated_at__isnull=True,
                        pdc__start_date__gte=three_days_before,
                        pdc__hazard_type=HazardType.EARTHQUAKE,
                    )
                )
                .order_by("-pdc__created_at")
                .select_related("country"),
                many=True,
            ).data

        elif region:
            oddrin_data = OddrinSerializer(Oddrin.objects.all(), many=True).data
            pdc_data = PdcDisplacementSerializer(
                PdcDisplacement.objects.filter(
                    models.Q(
                        country__region__name=region,
                        pdc__status=Pdc.Status.ACTIVE,
                        pdc__start_date__gte=seven_days_before,
                        pdc__hazard_type__in=[HazardType.FLOOD, HazardType.CYCLONE],
                    )
                    | models.Q(
                        pdc__status=Pdc.Status.ACTIVE,
                        country__isnull=True,
                        pdc__start_date__gte=seven_days_before,
                        pdc__hazard_type__in=[HazardType.FLOOD, HazardType.CYCLONE],
                    )
                    | models.Q(
                        country__region__name=region,
                        pdc__status=Pdc.Status.ACTIVE,
                        pdc__start_date__gte=seven_days_before,
                        pdc__hazard_type__in=[HazardType.FLOOD, HazardType.CYCLONE],
                    )
                    | models.Q(
                        pdc__status=Pdc.Status.ACTIVE,
                        country__isnull=True,
                        pdc__pdc_updated_at__isnull=True,
                        pdc__start_date__gte=seven_days_before,
                        pdc__hazard_type__in=[HazardType.FLOOD, HazardType.CYCLONE],
                    )
                    | models.Q(
                        country__region__name=region,
                        pdc__status=Pdc.Status.ACTIVE,
                        pdc__start_date__gte=three_days_before,
                        pdc__hazard_type=HazardType.EARTHQUAKE,
                    )
                    | models.Q(
                        pdc__status=Pdc.Status.ACTIVE,
                        country__isnull=True,
                        pdc__start_date__gte=three_days_before,
                        pdc__hazard_type=HazardType.EARTHQUAKE,
                    )
                    | models.Q(
                        country__region__name=region,
                        pdc__status=Pdc.Status.ACTIVE,
                        pdc__start_date__gte=three_days_before,
                        pdc__hazard_type=HazardType.EARTHQUAKE,
                    )
                    | models.Q(
                        pdc__status=Pdc.Status.ACTIVE,
                        country__isnull=True,
                        pdc__pdc_updated_at__isnull=True,
                        pdc__start_date__gte=three_days_before,
                        pdc__hazard_type=HazardType.EARTHQUAKE,
                    )
                )
                .order_by("-pdc__created_at")
                .select_related("country"),
                many=True,
            ).data

        else:
            oddrin_data = OddrinSerializer(Oddrin.objects.all(), many=True).data
            pdc_data = PdcDisplacementSerializer(PdcDisplacement.objects.all().select_related("country"), many=True).data

        return response.Response(
            {
                "pdc_data": pdc_data,
                "oddrin_data": oddrin_data,
            }
        )


class AdamViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdamSerializer
    filterset_class = AdamFilterSet

    def get_queryset(self):
        today = datetime.now().date()
        seven_days_before = today + timedelta(days=-7)
        three_days_before = today + timedelta(days=-3)
        return (
            Adam.objects.filter(
                models.Q(
                    publish_date__gte=seven_days_before,
                    hazard_type=HazardType.FLOOD,
                )
                | models.Q(publish_date__gte=seven_days_before, hazard_type=HazardType.FLOOD, country__isnull=True)
                | models.Q(
                    publish_date__gte=seven_days_before,
                    hazard_type=HazardType.CYCLONE,
                )
                | models.Q(publish_date__gte=seven_days_before, hazard_type=HazardType.CYCLONE, country__isnull=True)
                | models.Q(
                    publish_date__gte=three_days_before,
                    hazard_type=HazardType.EARTHQUAKE,
                )
                | models.Q(publish_date__gte=three_days_before, hazard_type=HazardType.EARTHQUAKE, country__isnull=True)
            )
            .order_by("event_id", "-publish_date")
            .distinct("event_id")
        )

    @extend_schema(request=None, responses=AdamExposureSerializer)
    @action(detail=True, url_path="exposure")
    def get_displacement(self, request, pk):
        object = self.get_object()
        data = {
            "storm_position_geojson": object.storm_position_geojson or None,
            "population_exposure": object.population_exposure or None,
        }
        return response.Response(data)


class PdcViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PdcSerializer
    filterset_class = PdcFilterSet

    def get_queryset(self):
        today = datetime.now().date()
        seven_days_before = today + timedelta(days=-7)
        three_days_before = today + timedelta(days=-3)
        queryset = (
            Pdc.objects.filter(
                models.Q(
                    status=Pdc.Status.ACTIVE,
                    start_date__gte=seven_days_before,
                    hazard_type=HazardType.FLOOD,
                )
                | models.Q(
                    status=Pdc.Status.ACTIVE,
                    pdcdisplacement__country__isnull=True,
                    start_date__gte=seven_days_before,
                    hazard_type=HazardType.FLOOD,
                )
                | models.Q(
                    status=Pdc.Status.ACTIVE,
                    start_date__gte=three_days_before,
                    hazard_type=HazardType.EARTHQUAKE,
                )
                | models.Q(
                    status=Pdc.Status.ACTIVE,
                    pdcdisplacement__country__isnull=True,
                    start_date__gte=three_days_before,
                    hazard_type=HazardType.EARTHQUAKE,
                )
                | models.Q(status=Pdc.Status.ACTIVE, end_date__gte=today, hazard_type=HazardType.CYCLONE)
                | models.Q(
                    status=Pdc.Status.ACTIVE,
                    pdcdisplacement__country__isnull=True,
                    end_date__gte=today,
                    hazard_type=HazardType.CYCLONE,
                )
                | models.Q(
                    status=Pdc.Status.ACTIVE,
                    start_date__gte=three_days_before,
                    hazard_type=HazardType.WILDFIRE,
                )
                | models.Q(
                    status=Pdc.Status.ACTIVE,
                    pdcdisplacement__country__isnull=True,
                    start_date__gte=three_days_before,
                    hazard_type=HazardType.WILDFIRE,
                )
            )
            .order_by("uuid", "-created_at")
            .distinct("uuid")
        )
        return queryset

    @extend_schema(request=None, responses=PdcExposureSerializer)
    @action(detail=True, url_path="exposure")
    def get_displacement(self, request, pk):
        object = self.get_object()
        displacement_data = PdcDisplacement.objects.filter(pdc=object.id).order_by("-pdc__pdc_updated_at")
        population_exposure = None
        capital_exposure = None
        if displacement_data.exists():
            population_exposure = displacement_data[0].population_exposure or None
            capital_exposure = displacement_data[0].capital_exposure or None
            if population_exposure.get("total"):
                population_exposure = population_exposure
            else:
                population_exposure = None
            if capital_exposure.get("total"):
                capital_exposure = capital_exposure
            else:
                capital_exposure = None
        data = {
            "footprint_geojson": object.footprint_geojson or None,
            "storm_position_geojson": object.storm_position_geojson or None,
            "population_exposure": population_exposure,
            "capital_exposure": capital_exposure,
        }
        return response.Response(PdcExposureSerializer(data).data)


class GDACSViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GDACSSeralizer
    filterset_class = GDACSFilterSet

    def get_queryset(self):
        today = datetime.now().date()
        seven_days_before = today + timedelta(days=-7)
        three_days_before = today + timedelta(days=-3)
        queryset = (
            GDACS.objects.filter(
                models.Q(
                    end_date__gte=seven_days_before,
                    hazard_type=HazardType.FLOOD,
                )
                | models.Q(
                    country__isnull=True,
                    end_date__gte=seven_days_before,
                    hazard_type=HazardType.FLOOD,
                )
                | models.Q(
                    end_date__gte=three_days_before,
                    hazard_type=HazardType.EARTHQUAKE,
                )
                | models.Q(
                    country__isnull=True,
                    end_date__gte=three_days_before,
                    hazard_type=HazardType.EARTHQUAKE,
                )
                | models.Q(
                    end_date__gte=seven_days_before,
                    hazard_type=HazardType.CYCLONE,
                )
                | models.Q(
                    country__isnull=True,
                    end_date__gte=seven_days_before,
                    hazard_type=HazardType.CYCLONE,
                )
                | models.Q(
                    end_date__gte=three_days_before,
                    hazard_type=HazardType.DROUGHT,
                )
                | models.Q(
                    country__isnull=True,
                    end_date__gte=three_days_before,
                    hazard_type=HazardType.DROUGHT,
                )
                | models.Q(
                    end_date__gte=three_days_before,
                    hazard_type=HazardType.WILDFIRE,
                )
                | models.Q(
                    country__isnull=True,
                    end_date__gte=three_days_before,
                    hazard_type=HazardType.FLOOD,
                )
            )
            .order_by("-created_at")
            .distinct()
        )
        return queryset

    @extend_schema(request=None, responses=GDACSExposureSerializer)
    @action(detail=True, url_path="exposure")
    def get_displacement(self, request, pk):
        object = self.get_object()
        data = {
            "footprint_geojson": object.footprint_geojson or None,
            "population_exposure": object.population_exposure or None,
        }
        return response.Response(data)


class MeteoSwissViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MeteoSwissAggSerializer
    filterset_class = MeteoSwissAggFilterSet

    def get_queryset(self):
        today = datetime.now().date()
        two_days_before = today + timedelta(days=-2)
        return (
            MeteoSwissAgg.objects.select_related("country")
            .filter(country__region__isnull=False, updated_at__gte=two_days_before)
            .distinct("country", "hazard_name")
        )

    @extend_schema(request=None, responses=MeteoSwissFootprintSerializer)
    @action(detail=True, url_path="exposure")
    def get_displacement(self, request, pk):
        object = self.get_object()
        data = {
            "footprint_geojson": object.geojson_details or None,
        }
        return response.Response(data)


class GWISViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GWISSerializer
    filterset_class = GWISFilterSet

    def get_queryset(self):
        return GWIS.objects.select_related("country")


@extend_schema_view(
    get=extend_schema(parameters=[CountryImminentRequestSerializer], responses=CountryImminentSerializer),
)
class CountryImminentViewSet(APIView):
    def get(self, request, *args, **kwargs):
        today = datetime.now().date()
        seven_days_before = today + timedelta(days=-7)
        three_days_before = today + timedelta(days=-3)
        two_days_before = today + timedelta(days=-2)
        iso3 = self.request.query_params.get("iso3")
        if iso3:
            pdc_count = (
                Pdc.objects.filter(
                    models.Q(
                        status=Pdc.Status.ACTIVE,
                        pdcdisplacement__country__iso3__icontains=iso3,
                        start_date__gte=seven_days_before,
                        hazard_type=HazardType.FLOOD,
                    )
                    | models.Q(
                        status=Pdc.Status.ACTIVE,
                        pdcdisplacement__country__iso3__icontains=iso3,
                        start_date__gte=three_days_before,
                        hazard_type=HazardType.EARTHQUAKE,
                    )
                    | models.Q(
                        status=Pdc.Status.ACTIVE,
                        pdcdisplacement__country__iso3__icontains=iso3,
                        end_date__gte=today,
                        hazard_type=HazardType.CYCLONE,
                    )
                    | models.Q(
                        status=Pdc.Status.ACTIVE,
                        pdcdisplacement__country__iso3__icontains=iso3,
                        start_date__gte=three_days_before,
                        hazard_type=HazardType.WILDFIRE,
                    )
                )
                .distinct()
                .count()
            )
            meteoswiss_count = (
                MeteoSwissAgg.objects.filter(
                    country__region__isnull=False,
                    latitude__isnull=False,
                    longitude__isnull=False,
                    updated_at__gte=two_days_before,
                    country__iso3__icontains=iso3,
                )
                .distinct()
                .count()
            )
            gdacs_count = (
                GDACS.objects.filter(
                    models.Q(end_date__gte=seven_days_before, hazard_type=HazardType.FLOOD, country__iso3__icontains=iso3)
                    | models.Q(end_date__gte=three_days_before, hazard_type=HazardType.EARTHQUAKE, country__iso3__icontains=iso3)
                    | models.Q(end_date__gte=seven_days_before, hazard_type=HazardType.CYCLONE, country__iso3__icontains=iso3)
                    | models.Q(end_date__gte=three_days_before, hazard_type=HazardType.DROUGHT, country__iso3__icontains=iso3)
                    | models.Q(end_date__gte=three_days_before, hazard_type=HazardType.WILDFIRE, country__iso3__icontains=iso3)
                )
                .distinct()
                .count()
            )
            adam_count = (
                Adam.objects.filter(
                    models.Q(publish_date__gte=seven_days_before, hazard_type=HazardType.FLOOD, country__iso3__icontains=iso3)
                    | models.Q(publish_date__gte=seven_days_before, hazard_type=HazardType.CYCLONE, country__iso3__icontains=iso3)
                    | models.Q(
                        publish_date__gte=three_days_before, hazard_type=HazardType.EARTHQUAKE, country__iso3__icontains=iso3
                    )
                )
                .distinct()
                .count()
            )
        else:
            pdc_count = 0
            gdacs_count = 0
            adam_count = 0
            meteoswiss_count = 0

        data = {"gdacs": gdacs_count, "pdc": pdc_count, "adam": adam_count, "meteoswiss": meteoswiss_count}
        return response.Response(CountryImminentSerializer(data).data)
