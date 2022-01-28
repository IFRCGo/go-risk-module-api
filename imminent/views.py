from datetime import timedelta, datetime

from rest_framework import viewsets, response

from django_filters.rest_framework import DjangoFilterBackend

from imminent.models import (
    Oddrin,
    PdcDisplacement,
    Pdc,
    Earthquake,
)
from imminent.serializers import (
    OddrinSerializer,
    PdcDisplacementSerializer,
    EarthquakeSerializer
)
from imminent.filter_set import EarthquakeFilterSet


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
        iso3 = self.request.query_params.get('iso3')
        hazard_type = self.request.query_params.get('hazard_type')
        today = datetime.now().date()
        yesterday = today + timedelta(days=-1)
        if iso3:
            oddrin_data = OddrinSerializer(
                Oddrin.objects.filter(
                    iso3__icontains=iso3
                ), many=True
            ).data
            pdc_data = PdcDisplacementSerializer(
                PdcDisplacement.objects.filter(
                    country__iso3__icontains=iso3,
                    pdc__status=Pdc.Status.ACTIVE
                ).order_by('-pdc__created_at').select_related('country').distinct('pdc__created_at'),
                many=True
            ).data

        else:
            oddrin_data = OddrinSerializer(
                Oddrin.objects.all(), many=True
            ).data
            pdc_data = PdcDisplacementSerializer(
                PdcDisplacement.objects.filter(
                    pdc__status=Pdc.Status.ACTIVE,
                ).select_related('country'),
                many=True
            ).data

        return response.Response(
            {
                'pdc_data': pdc_data,
                'oddrin_data': oddrin_data,
            }
        )
