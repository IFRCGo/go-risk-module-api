from rest_framework import viewsets, response
from django_filters.rest_framework import DjangoFilterBackend

from seasonal.models import (
    Idmc,
    InformRisk,
    IdmcSuddenOnset,
    InformRiskSeasonal,
    DisplacementData,
    GarHazardDisplacement,
    ThinkHazardInformation,
    GlobalDisplacement
)
from seasonal.serializers import (
    IdmcSerializer,
    InformRiskSerializer,
    IdmcSuddenOnsetSerializer,
    InformRiskSeasonalSerializer,
    DisplacementDataSerializer,
    GarHazardDisplacementSerializer,
    ThinkHazardInformationSerializer,
    GlobalDisplacementSerializer,
)


class IdmcViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Idmc.objects.all()
    serializer_class = IdmcSerializer


class InformRiskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InformRisk.objects.select_related('country')
    serializer_class = InformRiskSerializer


class IdmcSuddenOnsetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IdmcSuddenOnset.objects.select_related('country')
    serializer_class = IdmcSuddenOnsetSerializer


class InformRiskSeasonalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InformRiskSeasonal.objects.select_related('country')
    serializer_class = InformRiskSeasonalSerializer


class DisplacementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DisplacementData.objects.select_related('country')
    serializer_class = DisplacementDataSerializer


class GarHazardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GarHazardDisplacement.objects.select_related('country')
    serializer_class = GarHazardDisplacementSerializer


class GlobalDisplacementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GlobalDisplacementSerializer
    queryset = GlobalDisplacement.objects.all()


class ThinkHazardInformationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ThinkHazardInformationSerializer
    queryset = ThinkHazardInformation.objects.all()


class SeasonalViewSet(viewsets.ViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('iso3', 'hazard_type')

    def list(self, request, *args, **kwargs):
        iso3 = self.request.query_params.get('iso3')
        region = self.request.query_params.get('region')
        #hazard_type = self.request.query_params.get('hazard_type')
        if iso3 is not None:
            hazard_info = ThinkHazardInformationSerializer(
                ThinkHazardInformation.objects.filter(
                    country__iso3__icontains=iso3,
                ),
                many=True
            ).data
            inform = InformRiskSerializer(
                InformRisk.objects.filter(
                    country__iso3__icontains=iso3,
                ).select_related('country'),
                many=True
            ).data
            inform_seasonal = InformRiskSeasonalSerializer(
                InformRiskSeasonal.objects.filter(
                    country__iso3__icontains=iso3
                ).select_related('country'),
                many=True
            ).data
            idmc = IdmcSerializer(
                Idmc.objects.filter(
                    iso3__icontains=iso3,
                ),
                many=True
            ).data
            idmc_return_period_data = IdmcSuddenOnsetSerializer(
                IdmcSuddenOnset.objects.filter(
                    country__iso3__icontains=iso3
                ).select_related('country'),
                many=True
            ).data
            gar_return_period_data = GarHazardDisplacementSerializer(
                GarHazardDisplacement.objects.filter(
                    country__iso3__icontains=iso3
                ).select_related('country'),
                many=True
            ).data
            ipc_displacement_data = GlobalDisplacementSerializer(
                GlobalDisplacement.objects.filter(
                    country__iso3__icontains=iso3
                ).select_related('country'),
                many=True
            ).data
            raster_displacement_data = DisplacementDataSerializer(
                DisplacementData.objects.filter(
                    country__iso3__icontains=iso3
                ).select_related('country'),
                many=True
            ).data

        elif region:
            hazard_info = ThinkHazardInformationSerializer(
                ThinkHazardInformation.objects.filter(
                    country__region__region_id=region,
                ),
                many=True
            ).data
            inform = InformRiskSerializer(
                InformRisk.objects.filter(
                    country__region__region_id=region,
                ).select_related('country'),
                many=True
            ).data
            inform_seasonal = InformRiskSeasonalSerializer(
                InformRiskSeasonal.objects.filter(
                    country__region__region_id=region,
                ).select_related('country'),
                many=True
            ).data
            idmc = IdmcSerializer(
                Idmc.objects.filter(
                    country__region__region_id=region,
                ),
                many=True
            ).data
            idmc_return_period_data = IdmcSuddenOnsetSerializer(
                IdmcSuddenOnset.objects.filter(
                    country__region__region_id=region,
                ).select_related('country'),
                many=True
            ).data
            gar_return_period_data = GarHazardDisplacementSerializer(
                GarHazardDisplacement.objects.filter(
                    country__region__region_id=region,
                ).select_related('country'),
                many=True
            ).data
            ipc_displacement_data = GlobalDisplacementSerializer(
                GlobalDisplacement.objects.filter(
                    country__region__region_id=region,
                ).select_related('country'),
                many=True
            ).data
            raster_displacement_data = DisplacementDataSerializer(
                DisplacementData.objects.filter(
                    country__region__region_id=region,
                ).select_related('country'),
                many=True
            ).data

        else:
            hazard_info = ThinkHazardInformationSerializer(ThinkHazardInformation.objects.all(), many=True).data
            inform = InformRiskSerializer(InformRisk.objects.select_related('country'), many=True).data
            inform_seasonal = InformRiskSeasonalSerializer(InformRiskSeasonal.objects.select_related('country'), many=True).data
            idmc = IdmcSerializer(Idmc.objects.all(), many=True).data
            idmc_return_period_data = IdmcSuddenOnsetSerializer(IdmcSuddenOnset.objects.select_related('country'), many=True).data
            gar_return_period_data = GarHazardDisplacementSerializer(GarHazardDisplacement.objects.select_related('country'), many=True).data
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
