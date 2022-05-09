from rest_framework import viewsets, response
from django_filters.rest_framework import DjangoFilterBackend

from datetime import datetime
from datetime import timedelta
from openpyxl import Workbook
from django.http import HttpResponse
from common.models import HazardType
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
        #hazard_type = self.request.query_params.get('hazard_type')
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

        else:
            # hazard_info = ThinkHazardInformationSerializer(ThinkHazardInformation.objects.all(), many=True).data
            inform = InformRiskSerializer(InformRisk.objects.select_related('country'), many=True).data
            inform_seasonal = InformRiskSeasonalSerializer(InformRiskSeasonal.objects.select_related('country'), many=True).data
            idmc = IdmcSerializer(Idmc.objects.all(), many=True).data
            # idmc_return_period_data = IdmcSuddenOnsetSerializer(IdmcSuddenOnset.objects.select_related('country'), many=True).data
            return_period_data = GarHazardDisplacementSerializer(GarHazardDisplacement.objects.select_related('country'), many=True).data
            ipc_displacement_data = GlobalDisplacementSerializer(GlobalDisplacement.objects.select_related('country'), many=True).data
            raster_displacement_data = DisplacementDataSerializer(DisplacementData.objects.select_related('country'), many=True).data
        return response.Response(
            {
                'inform': inform,
                'inform_seasonal': inform_seasonal,
                'idmc': idmc,
                #'idmc_return_period': idmc_return_period_data,
                # 'hazard_info': hazard_info,
                'return_period_data': return_period_data,
                'ipc_displacement_data': ipc_displacement_data,
                'raster_displacement_data': raster_displacement_data,
            }
        )


def generate_data(request):
    exposure_queryset = DisplacementData.objects.all()
    displacement = Idmc.objects.all()
    all_data = []
    for exposure in exposure_queryset:
        for disp in displacement:
            if exposure.hazard_type == disp.hazard_type and exposure.country == disp.country:
                data = dict(
                    country=exposure.country.name,
                    hazard_type=exposure.hazard_type,
                    displacement_january=disp.january,
                    exposure_january=exposure.january,
                    displacement_february=disp.february,
                    exposure_february=exposure.february,
                    displacement_march=disp.march,
                    exposure_march=exposure.march,
                    displacement_april=disp.april,
                    exposure_april=exposure.april,
                    displacement_may=disp.may,
                    exposure_may=exposure.may,
                    displacement_june=disp.june,
                    exposure_june=exposure.june,
                    displacement_july=disp.july,
                    exposure_july=exposure.july,
                    displacement_august=disp.august,
                    exposure_august=exposure.august,
                    displacement_september=disp.september,
                    exposure_september=exposure.september,
                    displacement_october=disp.october,
                    exposure_october=exposure.october,
                    displacement_november=disp.november,
                    exposure_november=exposure.november,
                    displacement_december=disp.december,
                    exposure_december=exposure.december
                )
                all_data.append(data)
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={date}-summary.xlsx'.format(
        date=datetime.now().strftime('%Y-%m-%d'),
    )
    workbook = Workbook()

    worksheet = workbook.active
    worksheet.title = 'Customer'

    header_font = Font(name='Calibri', bold=True)

    columns = [
        ('country', 20),
        ('hazard_type', 20),
        ('displacement_january', 20),
        ('exposure_january', 20),
        ('displacement_february', 20),
        ('exposure_february',20),
        ('displacement_march',20),
        ('exposure_march',20),
        ('displacement_april',20),
        ('exposure_april',20),
        ('displacement_may',20),
        ('exposure_may',20),
        ('displacement_june',20),
        ('exposure_june',20),
        ('displacement_july',20),
        ('exposure_july',20),
        ('displacement_august',20),
        ('exposure_august',20),
        ('displacement_september',20),
        ('exposure_september',20),
        ('displacement_october',20),
        ('exposure_october',20),
        ('displacement_november',20),
        ('exposure_november',20),
        ('displacement_december',20),
        ('exposure_december',20),
    ]

    row_num = 1

    for col_num, (column_title,  column_width) in enumerate(columns, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title
        cell.font = header_font
        column_letter = get_column_letter(col_num)
        column_dimensions = worksheet.column_dimensions[column_letter]
        column_dimensions.width = column_width

    for customer in all_data:
        row_num += 1

        row = [
            customer['country'],
            customer['hazard_type'],
            customer['displacement_january'],
            customer['exposure_january'],
            customer['displacement_february'],
            customer['exposure_february']
        ]

        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value
    workbook.save(response)
    return response
