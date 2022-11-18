from datetime import timedelta, datetime

from rest_framework import viewsets, response
from rest_framework.pagination import LimitOffsetPagination

from django_filters.rest_framework import DjangoFilterBackend
from django.db import models

from imminent.models import (
    Oddrin,
    PdcDisplacement,
    Pdc,
    Earthquake,
    Adam,
)
from imminent.serializers import (
    OddrinSerializer,
    PdcDisplacementSerializer,
    EarthquakeSerializer,
    AdamSerializer,
)
from imminent.filter_set import (
    EarthquakeFilterSet,
    AdamFilterSet,
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
        today = datetime.now().date()
        yesterday = today + timedelta(days=-1)
        return PdcDisplacement.objects.filter(
            pdc__status=Pdc.Status.ACTIVE,
        ).select_related('country')


class ImminentViewSet(viewsets.ViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('iso3', 'hazard_type')

    def list(self, request, *args, **kwargs):
        today = datetime.now().date()
        seven_days_before = today + timedelta(days=-7)
        iso3 = self.request.query_params.get('iso3')
        region = self.request.query_params.get('region')
        if iso3:
            oddrin_data = OddrinSerializer(
                Oddrin.objects.filter(
                    iso3__icontains=iso3
                ), many=True
            ).data
            pdc_data = PdcDisplacementSerializer(
                PdcDisplacement.objects.filter(
                    models.Q(
                        country__iso3__icontains=iso3,
                        pdc__status=Pdc.Status.ACTIVE,
                        pdc__pdc_updated_at__gte=seven_days_before,
                    ) | models.Q(
                        country__iso3__icontains=iso3,
                        pdc__status=Pdc.Status.ACTIVE,
                        pdc__pdc_updated_at__isnull=True,
                        pdc__pdc_created_at__gte=seven_days_before,
                    )
                ).order_by('-pdc__created_at').select_related('country'),
                many=True
            ).data

        elif region:
            oddrin_data = OddrinSerializer(
                Oddrin.objects.all(), many=True
            ).data
            pdc_data = PdcDisplacementSerializer(
                PdcDisplacement.objects.filter(
                    models.Q(
                        country__region__name=region,
                        pdc__status=Pdc.Status.ACTIVE,
                        pdc__pdc_updated_at__gte=seven_days_before,
                    ) | models.Q(
                        pdc__status=Pdc.Status.ACTIVE,
                        country__isnull=True,
                        pdc__pdc_updated_at__gte=seven_days_before,
                    ) |
                    models.Q(
                        country__region__name=region,
                        pdc__status=Pdc.Status.ACTIVE,
                        pdc__pdc_created_at__gte=seven_days_before,
                    ) | models.Q(
                        pdc__status=Pdc.Status.ACTIVE,
                        country__isnull=True,
                        pdc__pdc_updated_at__isnull=True,
                        pdc__pdc_created_at__gte=seven_days_before,
                    )
                ).order_by('-pdc__created_at').select_related('country'),
                many=True
            ).data

        else:
            oddrin_data = OddrinSerializer(
                Oddrin.objects.all(), many=True
            ).data
            pdc_data = PdcDisplacementSerializer(
                PdcDisplacement.objects.all().select_related('country'),
                many=True
            ).data

        return response.Response(
            {
                'pdc_data': pdc_data,
                'oddrin_data': oddrin_data,
            }
        )


class AdamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Adam.objects.select_related('country')
    serializer_class = AdamSerializer
    filteset_class = AdamFilterSet
