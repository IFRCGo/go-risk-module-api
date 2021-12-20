from rest_framework import viewsets

from earthquake.models import Earthquake
from earthquake.serializers import EarthquakeSerializer
from earthquake.filter_set import EarthquakeFilterSet


class EarthquakeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Earthquake.objects.all()
    serializer_class = EarthquakeSerializer
    filterset_class = EarthquakeFilterSet
