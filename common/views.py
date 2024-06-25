from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from risk_module.enums import GlobalEnumSerializer, get_enum_values


class GlobalEnumView(APIView):
    """
    Provide a single endpoint to fetch enum metadata
    """

    @extend_schema(responses=GlobalEnumSerializer)
    def get(self, _):
        """
        Return a list of all enums.
        """
        return Response(get_enum_values())
