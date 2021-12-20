from rest_framework import serializers

from earthquake.models import Earthquake


class EarthquakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Earthquake
        fields = '__all__'
