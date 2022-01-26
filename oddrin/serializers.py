import os
import subprocess

#from osgeo import gdal
from rest_framework import serializers

from django.conf import settings

from oddrin.models import (
    Oddrin,
    Idmc,
    InformRisk,
    IdmcSuddenOnset,
    InformRiskSeasonal,
    RiskFile,
    DisplacementData,
    GarHazardDisplacement,
    PdcDisplacement,
    Pdc,
)
#from oddrin.scripts import get_cloud_optimized_file

from ipc.serializers import CountrySerializer, GlobalDisplacementSerializer, ThinkHazardInformationSerializer
#from oddrin.scripts.create_raster_tile import create_raster_tile


def get_cloud_optimized_file(file):
    destination_file = os.path.join(settings.BASE_DIR, 'media/test', 'test.tif')
    scaled_command_using_glad = f'gdalwarp {file} {destination_file} -of COG'
    data = subprocess.Popen(scaled_command_using_glad, stdout=subprocess.PIPE, shell=True)
    _, tail = os.path.split(destination_file)
    return os.path.join('oddrin/cog_files', tail)


class RiskFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskFile
        fields = '__all__'


class OddrinSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display', read_only=True)
    file_type_display = serializers.CharField(source='get_file_type_display', read_only=True)

    class Meta:
        model = Oddrin
        fields = '__all__'

    def create(self, validated_data):
        """file = validated_data.get('file')
        if file:
            cog_file = get_cloud_optimized_file(file)
            validated_data['cog_file'] = cog_file"""
        return super().create(validated_data)


class IdmcSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    confidence_type_display = serializers.CharField(source='get_confidence_type_display')

    class Meta:
        model = Idmc
        fields = '__all__'


class InformRiskSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    country_details = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = InformRisk
        fields = '__all__'


class IdmcSuddenOnsetSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    country_details = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = IdmcSuddenOnset
        fields = '__all__'


class InformRiskSeasonalSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    country_details = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = InformRiskSeasonal
        fields = '__all__'


class DisplacementDataSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    country_details = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = DisplacementData
        fields = '__all__'


class GarHazardDisplacementSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    country_details = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = GarHazardDisplacement
        fields = '__all__'


class PdcSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display')

    class Meta:
        model = Pdc
        fields = '__all__'


class PdcDisplacementSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source='get_hazard_type_display')
    country_details = CountrySerializer(source='country', read_only=True)
    pdc_details = PdcSerializer(source='pdc', read_only=True)

    class Meta:
        model = PdcDisplacement
        fields = '__all__'
