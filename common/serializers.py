from rest_framework import serializers

from common.models import Country, Region


class RegionSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source="get_name_display", read_only=True)

    class Meta:
        model = Region
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    # region_details = RegionSerializer(source='region', read_only=True)

    class Meta:
        model = Country
        fields = (
            "id",
            "name",
            "iso",
            "iso3",
            "region",
        )
