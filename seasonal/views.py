from rest_framework import viewsets, response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from datetime import datetime
from datetime import timedelta
from openpyxl import Workbook
from django.http import HttpResponse
from common.models import HazardType
from django.db import models
from seasonal.models import (
    Idmc,
    InformRisk,
    IdmcSuddenOnset,
    InformRiskSeasonal,
    DisplacementData,
    GarHazardDisplacement,
    ThinkHazardInformation,
    GlobalDisplacement,
    GarProbabilistic,
    PossibleEarlyActions,
    PublishReport,
    PublishReportProgram,
    PossibleEarlyActionsSectors,
    RiskScore
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
    GarProbabilisticSerializer,
    PossibleEarlyActionsSerializer,
    PublishReportSerializer,
    RiskScoreSerializer,
)
from seasonal.filter_set import (
    PossibleEarlyActionsFilterSet,
    PublishReportFilterSet,
    RiskScoreFilterSet,
)
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from openpyxl.utils import get_column_letter

from django.http import HttpResponse

from datetime import date, timedelta, datetime


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
        # hazard_type = self.request.query_params.get('hazard_type')
        if iso3 is not None:
            """hazard_info = ThinkHazardInformationSerializer(
                ThinkHazardInformation.objects.filter(
                    country__iso3__icontains=iso3,
                ),
                many=True
            ).data"""
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
            """idmc_return_period_data = IdmcSuddenOnsetSerializer(
                IdmcSuddenOnset.objects.filter(
                    country__iso3__icontains=iso3
                ).select_related('country'),
                many=True
            ).data"""
            return_period_data = GarHazardDisplacementSerializer(
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
            gar_loss = GarProbabilisticSerializer(
                GarProbabilistic.objects.filter(
                    country__iso3__icontains=iso3
                ).select_related('country'),
                many=True
            ).data

        elif region:
            """hazard_info = ThinkHazardInformationSerializer(
                ThinkHazardInformation.objects.filter(
                    country__region__name=region,
                ),
                many=True
            ).data"""
            inform = InformRiskSerializer(
                InformRisk.objects.filter(
                    country__region__name=region,
                ).select_related('country'),
                many=True
            ).data
            inform_seasonal = InformRiskSeasonalSerializer(
                InformRiskSeasonal.objects.filter(
                    country__region__name=region,
                ).select_related('country'),
                many=True
            ).data
            idmc = IdmcSerializer(
                Idmc.objects.filter(
                    country__region__name=region,
                ),
                many=True
            ).data
            """idmc_return_period_data = IdmcSuddenOnsetSerializer(
                IdmcSuddenOnset.objects.filter(
                    country__region__name=region,
                ).select_related('country'),
                many=True
            ).data"""
            return_period_data = GarHazardDisplacementSerializer(
                GarHazardDisplacement.objects.filter(
                    country__region__name=region,
                ).select_related('country'),
                many=True
            ).data
            ipc_displacement_data = GlobalDisplacementSerializer(
                GlobalDisplacement.objects.filter(
                    country__region=region,
                ).select_related('country'),
                many=True
            ).data
            raster_displacement_data = DisplacementDataSerializer(
                DisplacementData.objects.filter(
                    country__region__name=region,
                ).select_related('country'),
                many=True
            ).data
            gar_loss = GarProbabilisticSerializer(
                GarProbabilistic.objects.filter(
                    country__region__name=region,
                ).select_related('country'),
                many=True
            ).data

        else:
            # hazard_info = ThinkHazardInformationSerializer(ThinkHazardInformation.objects.all(), many=True).data
            inform = InformRiskSerializer(InformRisk.objects.select_related('country'), many=True).data
            inform_seasonal = InformRiskSeasonalSerializer(InformRiskSeasonal.objects.select_related('country'), many=True).data
            idmc = IdmcSerializer(Idmc.objects.all(), many=True).data
            # idmc_return_period_data = IdmcSuddenOnsetSerializer(IdmcSuddenOnset.objects.select_related('country'), many=True).data
            return_period_data = GarHazardDisplacementSerializer(GarHazardDisplacement.objects.select_related('country'), many=True).data
            ipc_displacement_data = GlobalDisplacementSerializer(GlobalDisplacement.objects.select_related('country'), many=True).data
            raster_displacement_data = DisplacementDataSerializer(DisplacementData.objects.select_related('country'), many=True).data
            gar_loss = GarProbabilisticSerializer(GarProbabilistic.objects.select_related('country'), many=True).data
        return response.Response(
            {
                'inform': inform,
                'inform_seasonal': inform_seasonal,
                'idmc': idmc,
                # 'idmc_return_period': idmc_return_period_data,
                # 'hazard_info': hazard_info,
                'return_period_data': return_period_data,
                'ipc_displacement_data': ipc_displacement_data,
                'raster_displacement_data': raster_displacement_data,
                'gar_loss': gar_loss,
            }
        )


def generate_data(request):
    exposure_queryset = DisplacementData.objects.filter(
        models.Q(hazard_type=HazardType.FLOOD) | models.Q(hazard_type=HazardType.CYCLONE)
    )
    ipc_displacement = GlobalDisplacement.objects.filter(
        hazard_type=HazardType.FOOD_INSECURITY
    )
    all_data = []
    for exposure in exposure_queryset:
        data = dict(
            country=exposure.country.name,
            hazard_type=exposure.hazard_type,
            exposure_january=exposure.january,
            exposure_february=exposure.february,
            exposure_march=exposure.march,
            exposure_april=exposure.april,
            exposure_may=exposure.may,
            exposure_june=exposure.june,
            exposure_july=exposure.july,
            exposure_august=exposure.august,
            exposure_september=exposure.september,
            exposure_october=exposure.october,
            exposure_november=exposure.november,
            exposure_december=exposure.december,
            year='',
        )
        all_data.append(data)
    for ipc_data in ipc_displacement:
        new_data = dict(
            country=ipc_data.country.name,
            hazard_type=ipc_data.hazard_type,
            exposure_january=ipc_data.total_displacement if ipc_data.month == 1 else '',
            exposure_february=ipc_data.total_displacement if ipc_data.month == 2 else '',
            exposure_march=ipc_data.total_displacement if ipc_data.month == 3 else '',
            exposure_april=ipc_data.total_displacement if ipc_data.month == 4 else '',
            exposure_may=ipc_data.total_displacement if ipc_data.month == 5 else '',
            exposure_june=ipc_data.total_displacement if ipc_data.month == 6 else '',
            exposure_july=ipc_data.total_displacement if ipc_data.month == 7 else '',
            exposure_august=ipc_data.total_displacement if ipc_data.month == 8 else '',
            exposure_september=ipc_data.total_displacement if ipc_data.month == 9 else '',
            exposure_october=ipc_data.total_displacement if ipc_data.month == 10 else '',
            exposure_november=ipc_data.total_displacement if ipc_data.month == 11 else '',
            exposure_december=ipc_data.total_displacement if ipc_data.month == 12 else '',
            year=ipc_data.year
        )
        all_data.append(new_data)
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={date}-exposure-summary.xlsx'.format(
        date=datetime.now().strftime('%Y-%m-%d'),
    )
    workbook = Workbook()

    worksheet = workbook.active
    worksheet.title = 'Exposure Data'

    header_font = Font(name='Calibri', bold=True)

    columns = [
        ('country', 20),
        ('hazard_type', 20),
        ('exposure_january', 20),
        ('exposure_february', 20),
        ('exposure_march', 20),
        ('exposure_april', 20),
        ('exposure_may', 20),
        ('exposure_june', 20),
        ('exposure_july', 20),
        ('exposure_august', 20),
        ('exposure_september', 20),
        ('exposure_october', 20),
        ('exposure_november', 20),
        ('exposure_december', 20),
        ('year', 20),
    ]

    row_num = 1

    for col_num, (column_title,  column_width) in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title
        cell.font = header_font
        column_letter = get_column_letter(col_num)
        column_dimensions = worksheet.column_dimensions[column_letter]
        column_dimensions.width = column_width

    for event in all_data:
        row_num += 1
        row = [
            event['country'],
            event['hazard_type'],
            event['exposure_january'],
            event['exposure_february'],
            event['exposure_march'],
            event['exposure_april'],
            event['exposure_may'],
            event['exposure_june'],
            event['exposure_july'],
            event['exposure_august'],
            event['exposure_september'],
            event['exposure_october'],
            event['exposure_november'],
            event['exposure_december'],
            event['year'],
        ]

        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value
    workbook.save(response)
    return response


class EarlyActionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PossibleEarlyActions.objects.select_related('country')
    filterset_class = PossibleEarlyActionsFilterSet
    serializer_class = PossibleEarlyActionsSerializer

    @action(
        detail=False,
        url_path='options'
    )
    def get_options(self, request, **kwargs):
        options = {
            'sectors': [
                {
                    'id': sector.id,
                    'name': sector.name,
                } for sector in PossibleEarlyActionsSectors.objects.all().distinct('name')
            ],
        }

        return response.Response(options)


class PublishReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PublishReport.objects.all()
    filterset_class = PublishReportFilterSet
    serializer_class = PublishReportSerializer


class RiskScoreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RiskScore.objects.select_related('country')
    serializer_class = RiskScoreSerializer
    filterset_class = RiskScoreFilterSet
