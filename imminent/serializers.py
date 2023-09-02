from rest_framework import serializers

from imminent.models import (
    Oddrin,
    PdcDisplacement,
    Pdc,
    Earthquake,
    Adam,
    GDACS,
    MeteoSwiss,
    MeteoSwissAgg,
    GWIS,
)

from common.serializers import CountrySerializer


"""
def get_cloud_optimized_file(file):
    destination_file = os.path.join(settings.BASE_DIR, 'media/test', 'test.tif')
    scaled_command_using_glad = f'gdalwarp {file} {destination_file} -of COG'
    data = subprocess.Popen(scaled_command_using_glad, stdout=subprocess.PIPE, shell=True)
    _, tail = os.path.split(destination_file)
    return os.path.join('oddrin/cog_files', tail)"""


class OddrinSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source="get_hazard_type_display", read_only=True)
    file_type_display = serializers.CharField(source="get_file_type_display", read_only=True)

    class Meta:
        model = Oddrin
        fields = "__all__"


class PdcSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    severity_display = serializers.CharField(source="get_severity_display", read_only=True)

    class Meta:
        model = Pdc
        exclude = [
            "footprint_geojson",
            "storm_position_geojson",
        ]


class PdcDisplacementSerializer(serializers.ModelSerializer):
    hazard_type_display = serializers.CharField(source="get_hazard_type_display")
    country_details = CountrySerializer(source="country", read_only=True)
    pdc_details = PdcSerializer(source="pdc", read_only=True)

    class Meta:
        model = PdcDisplacement
        fields = "__all__"


class EarthquakeSerializer(serializers.ModelSerializer):
    country_details = CountrySerializer(source="country", read_only=True)

    class Meta:
        model = Earthquake
        fields = "__all__"


class AdamSerializer(serializers.ModelSerializer):
    country_details = CountrySerializer(source="country", read_only=True)
    hazard_type_display = serializers.CharField(source="get_hazard_type_display")

    class Meta:
        model = Adam
        exclude = [
            "storm_position_geojson",
            "population_exposure",
        ]


class GDACSSeralizer(serializers.ModelSerializer):
    country_details = CountrySerializer(source="country", read_only=True)
    hazard_type_display = serializers.CharField(source="get_hazard_type_display")

    class Meta:
        model = GDACS
        exclude = [
            "footprint_geojson",
            "population_exposure",
        ]


class MeteoSwissAggSerializer(serializers.ModelSerializer):
    country_details = CountrySerializer(source="country", read_only=True)
    hazard_type_display = serializers.CharField(source="get_hazard_type_display")

    class Meta:
        model = MeteoSwissAgg
        exclude = [
            "geojson_details",
        ]


class GWISSerializer(serializers.ModelSerializer):
    country_details = CountrySerializer(source="country", read_only=True)
    hazard_type_display = serializers.CharField(source="get_hazard_type_display")

    class Meta:
        model = GWIS
        fields = "__all__"


class PdcExposureSerializer(serializers.Serializer):
    footprint_geojson = serializers.JSONField()
    storm_position_geojson = serializers.JSONField()
    population_exposure = serializers.JSONField()
    capital_exposure = serializers.JSONField()


class GDACSExposureSerializer(serializers.Serializer):
    footprint_geojson = serializers.JSONField()
    population_exposure = serializers.JSONField()


class AdamPopulationExposureSerializer(serializers.Serializer):
    exposure_60_kmh = serializers.FloatField(required=False, allow_null=True)
    exposure_90_kmh = serializers.FloatField(required=False, allow_null=True)
    exposure_120_kmh = serializers.FloatField(required=False, allow_null=True)


class AdamExposureSerializer(serializers.Serializer):
    storm_position_geojson = serializers.JSONField()
    population_exposure = AdamPopulationExposureSerializer(required=False)


class MeteoSwissFootprintSerializer(serializers.Serializer):
    footprint_geojson = serializers.JSONField(required=False)
