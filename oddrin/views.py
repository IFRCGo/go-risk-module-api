from django.db.models import Q

from datetime import timedelta, datetime

from rest_framework import viewsets, response

from django_filters.rest_framework import DjangoFilterBackend

from oddrin.models import (
    Oddrin,
    Idmc,
    InformRisk,
    IdmcSuddenOnset,
    InformRiskSeasonal,
    DisplacementData,
    GarHazard,
    PdcDisplacement,
    Pdc,
)
from ipc.models import (
    ThinkHazardInformation,
    GlobalDisplacement
)
from oddrin.serializers import (
    OddrinSerializer,
    IdmcSerializer,
    InformRiskSerializer,
    IdmcSuddenOnsetSerializer,
    InformRiskSeasonalSerializer,
    DisplacementDataSerializer,
    GarHazardSerializer,
    PdcDisplacementSerializer,
)
from oddrin.filter_set import (
    IdmcFilterSet,
    InformRiskFilterSet,
    IdmcSuddenOnsetFilterSet,
    InfromRiskSeasonalFilterSet,
    OddrinFilterSet,
    DisplacementDataFilterSet,
    GarHazardFilterSet,
    PdcDisplacemenFilterSet
)
from ipc.serializers import ThinkHazardInformationSerializer, GlobalDisplacementSerializer


class OddrinViewSet(viewsets.ModelViewSet):
    queryset = Oddrin.objects.all()
    serializer_class = OddrinSerializer
    filterset_class = OddrinFilterSet


class IdmcViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Idmc.objects.all()
    serializer_class = IdmcSerializer
    filterset_class = IdmcFilterSet


class InformRiskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InformRisk.objects.select_related('country')
    serializer_class = InformRiskSerializer
    filterset_class = InformRiskFilterSet


class IdmcSuddenOnsetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IdmcSuddenOnset.objects.select_related('country')
    serializer_class = IdmcSuddenOnsetSerializer
    filterset_class = IdmcSuddenOnsetFilterSet


class InformRiskSeasonalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InformRiskSeasonal.objects.select_related('country')
    serializer_class = InformRiskSeasonalSerializer
    filterset_class = InfromRiskSeasonalFilterSet


class DisplacementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DisplacementData.objects.select_related('country')
    serializer_class = DisplacementDataSerializer
    filterset_class = DisplacementDataFilterSet


class GarHazardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GarHazard.objects.select_related('country')
    serializer_class = GarHazardSerializer
    filterset_class = GarHazardFilterSet


class PdcDisplacementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PdcDisplacementSerializer
    filterset_class = PdcDisplacemenFilterSet

    def get_queryset(self):
        today = datetime.now().date()
        yesterday = today + timedelta(days=-1)
        return PdcDisplacement.objects.filter(
            pdc__created_at__date__lte=today,
            pdc__created_at__date__gte=yesterday,
            pdc__status=Pdc.Status.ACTIVE,
        ).select_related('country')


class SeasonalViewSet(viewsets.ViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('iso3', 'hazard_type')

    def list(self, request, *args, **kwargs):
        iso3 = self.request.query_params.get('iso3')
        hazard_type = self.request.query_params.get('hazard_type')
        if iso3 or hazard_type:
            hazard_info = ThinkHazardInformationSerializer(
                ThinkHazardInformation.objects.filter(
                    Q(country__iso3__icontains=iso3) |
                    Q(hazard_type=hazard_type)
                ),
                many=True
            ).data
            inform = InformRiskSerializer(
                InformRisk.objects.filter(
                    Q(country__iso3__icontains=iso3) |
                    Q(hazard_type=hazard_type)
                ).select_related('country'),
                many=True
            ).data
            inform_seasonal = InformRiskSeasonalSerializer(
                InformRiskSeasonal.objects.filter(
                    Q(country__iso3__icontains=iso3) |
                    Q(hazard_type=hazard_type)
                ).select_related('country'),
                many=True
            ).data
            idmc = IdmcSerializer(
                Idmc.objects.filter(
                    Q(iso3__icontains=iso3) |
                    Q(hazard_type=hazard_type)
                ),
                many=True
            ).data
            idmc_return_period_data = IdmcSuddenOnsetSerializer(
                IdmcSuddenOnset.objects.filter(
                    Q(country__iso3__icontains=iso3) |
                    Q(hazard_type=hazard_type)
                ).select_related('country'),
                many=True
            ).data
            gar_return_period_data = GarHazardSerializer(
                GarHazard.objects.filter(
                    Q(country__iso3__icontains=iso3) |
                    Q(hazard_type=hazard_type)
                ).select_related('country'),
                many=True
            ).data
            ipc_displacement_data = GlobalDisplacementSerializer(
                GlobalDisplacement.objects.filter(
                    Q(country__iso3__icontains=iso3) |
                    Q(hazard_type=hazard_type)
                ).select_related('country'),
                many=True
            ).data
            raster_displacement_data = DisplacementDataSerializer(
                DisplacementData.objects.filter(
                    Q(country__iso3__icontains=iso3) |
                    Q(hazard_type=hazard_type)
                ).select_related('country'),
                many=True
            ).data

        if iso3 and hazard_type:
            hazard_info = ThinkHazardInformationSerializer(
                ThinkHazardInformation.objects.filter(
                    country__iso3__icontains=iso3,
                    hazard_type=hazard_type
                ),
                many=True
            ).data
            inform = InformRiskSerializer(
                InformRisk.objects.filter(
                    country__iso3__icontains=iso3,
                    hazard_type=hazard_type
                ).select_related('country'),
                many=True
            ).data
            inform_seasonal = InformRiskSeasonalSerializer(
                InformRiskSeasonal.objects.filter(
                    country__iso3__icontains=iso3,
                    hazard_type=hazard_type
                ).select_related('country'),
                many=True
            ).data
            idmc = IdmcSerializer(
                Idmc.objects.filter(
                    iso3__icontains=iso3,
                    hazard_type=hazard_type
                ),
                many=True
            ).data
            idmc_return_period_data = IdmcSuddenOnsetSerializer(
                IdmcSuddenOnset.objects.filter(
                    country__iso3__icontains=iso3,
                    hazard_type=hazard_type
                ).select_related('country'),
                many=True
            ).data
            gar_return_period_data = GarHazardSerializer(
                GarHazard.objects.filter(
                    country__iso3__icontains=iso3,
                    hazard_type=hazard_type
                ).select_related('country'),
                many=True
            ).data
            ipc_displacement_data = GlobalDisplacementSerializer(
                GlobalDisplacement.objects.filter(
                    country__iso3__icontains=iso3,
                    hazard_type=hazard_type
                ).select_related('country'),
                many=True
            ).data
            raster_displacement_data = DisplacementDataSerializer(
                DisplacementData.objects.filter(
                    country__iso3__icontains=iso3,
                    hazard_type=hazard_type
                ).select_related('country'),
                many=True
            ).data
        else:
            hazard_info = ThinkHazardInformationSerializer(ThinkHazardInformation.objects.all(), many=True).data
            inform = InformRiskSerializer(InformRisk.objects.select_related('country'), many=True).data
            inform_seasonal = InformRiskSeasonalSerializer(InformRiskSeasonal.objects.select_related('country'), many=True).data
            idmc = IdmcSerializer(Idmc.objects.all(), many=True).data
            idmc_return_period_data = IdmcSuddenOnsetSerializer(IdmcSuddenOnset.objects.select_related('country'), many=True).data
            gar_return_period_data = GarHazardSerializer(GarHazard.objects.select_related('country'), many=True).data
            ipc_displacement_data = GlobalDisplacementSerializer(GlobalDisplacement.objects.select_related('country'), many=True).data
            raster_displacement_data = DisplacementDataSerializer(DisplacementData.objects.select_related('country'), many=True).data

        return response.Response(
            {
                'inform': inform,
                'inform_seasonal': inform_seasonal,
                'idmc': idmc,
                'idmc_return_period': idmc_return_period_data,
                'hazard_info': hazard_info,
                'gar_return_period_data': gar_return_period_data,
                'ipc_displacement_data': ipc_displacement_data,
                'raster_displacement_data': raster_displacement_data,
            }
        )


class ImminentViewSet(viewsets.ViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('iso3', 'hazard_type')

    def list(self, request, *args, **kwargs):
        iso3 = self.request.query_params.get('iso3')
        hazard_type = self.request.query_params.get('hazard_type')
        today = datetime.now().date()
        yesterday = today + timedelta(days=-1)
        if iso3 or hazard_type:
            oddrin_data = OddrinSerializer(
                Oddrin.objects.filter(
                    Q(iso3__icontains=iso3) |
                    Q(hazard_type=hazard_type)
                ), many=True
            ).data
            pdc_data = PdcDisplacementSerializer(
                PdcDisplacement.objects.filter(
                    Q(country__iso3__icontains=iso3,
                        pdc__created_at__date__lte=today,
                        pdc__created_at__date__gte=yesterday,
                        pdc__status=Pdc.Status.ACTIVE) |
                    Q(pdc__created_at__date__lte=today,
                        pdc__created_at__date__gte=yesterday,
                        pdc__status=Pdc.Status.ACTIVE,
                        hazard_type=hazard_type)
                ).select_related('country'),
                many=True
            ).data
        if iso3 and hazard_type:
            oddrin_data = OddrinSerializer(
                Oddrin.objects.filter(
                    iso3__icontains=iso3,
                    hazard_type=hazard_type
                ), many=True
            ).data
            pdc_data = PdcDisplacementSerializer(
                PdcDisplacement.objects.filter(
                    country__iso3__icontains=iso3,
                    pdc__created_at__date__lte=today,
                    pdc__created_at__date__gte=yesterday,
                    pdc__status=Pdc.Status.ACTIVE,
                    hazard_type=hazard_type
                ).select_related('country'),
                many=True
            ).data
        else:
            oddrin_data = OddrinSerializer(
                Oddrin.objects.all(), many=True
            ).data
            pdc_data = PdcDisplacementSerializer(
                PdcDisplacement.objects.filter(
                    pdc__created_at__date__lte=today,
                    pdc__created_at__date__gte=yesterday,
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
