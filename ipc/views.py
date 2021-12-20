from rest_framework import viewsets

from ipc.models import GlobalDisplacement, ThinkHazardInformation
from ipc.serializers import GlobalDisplacementSerializer, ThinkHazardInformationSerializer
from ipc.filter_set import GlobalDisplacementFilterSet, ThinkHazardInformationFilterSet


class GlobalDisplacementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GlobalDisplacementSerializer
    filterset_class = GlobalDisplacementFilterSet
    queryset = GlobalDisplacement.objects.all()


class ThinkHazardInformationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ThinkHazardInformationSerializer
    filterset_class = ThinkHazardInformationFilterSet
    queryset = ThinkHazardInformation.objects.all()
