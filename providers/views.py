from .models import Provider, Polygon
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProviderSerializer, PolygonSerializer, PointSerializer
from django.contrib.gis.geos import GEOSGeometry


class ProviderViewSet(viewsets.ModelViewSet):
    """
    API endpoint to CRUD the providers.
    User should be staff.
    """
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = (permissions.IsAdminUser,)


class PolygonViewSet(viewsets.ModelViewSet):
    """
    API endpoit to CRUD the polygons.
    """
    queryset = Polygon.objects.all()
    serializer_class = PolygonSerializer


class PointView(APIView):
    """
    Lists all polygons that contain a point.
    """
    def get(self, request):
        return Response()

    def post(self, request):
        point = GEOSGeometry(str(request.data))
        polygons = Polygon.objects.filter(geojson__contains=point)
        serializer = PolygonSerializer(polygons,
                                       many=True,
                                       context={'request': request}
                                      )
        return Response(serializer.data)
