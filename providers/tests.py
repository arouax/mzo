import json
from rest_framework import status
from rest_framework.test import APIRequestFactory
from django.test import TestCase, Client
from django.urls import reverse
from .models import Provider, Polygon
from .serializers import (
    PolygonSerializer,
    ProviderSerializer,
    PointSerializer,
)
from .views import (
    ProviderViewSet,
    PolygonViewSet,
    PointView,
)
from django.contrib.gis.geos import GEOSGeometry

client = Client()

class GetAllProvidersTest(TestCase):
    """
    Test module for GET all providers API
    """
    def setUp(self):
        Provider.objects.create(
            name='Provider1',
            email='email@example.com',
            phone='+77777777777',
            language='en',
            currency='USD',
            password='qwer1234'
        )
        Provider.objects.create(
            name='Provider2',
            email='email@example.com',
            phone='+77777777777',
            language='en',
            currency='USD',
            password='qwer1234'
        )
        Provider.objects.create(
            name='Provider3',
            email='email@example.com',
            phone='+77777777777',
            language='en',
            currency='USD',
            password='qwer1234'
        )

    def test_get_all_providers(self):
        response = client.get('/providers/')
        providers = Provider.objects.all()
        serializer = ProviderSerializer(providers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllPolygonsTest(TestCase):
    """
    Test module for GET all polygons API
    """
    def setUp(self):
        provider = Provider.objects.create(
            name='Provider1',
            email='email@example.com',
            phone='+77777777777',
            language='en',
            currency='USD',
            password='qwer1234',
        )
        Polygon.objects.create(
            name='Polygon1',
            price=10,
            provider=provider,
            geojson="""{ "type": "Polygon", "coordinates":
            [ [ [ 2.319192095177777, 48.864936200483115 ],
            [ 2.320809898983764, 48.867157194778059 ], [ 2.340926937614733,
            48.860910397075138 ], [ 2.33973116958422, 48.859013067110759 ],
            [ 2.330165025340123, 48.86081784606256 ],
            [ 2.319192095177777, 48.864936200483115 ] ] ] }""",
        )
        Polygon.objects.create(
            name='Polygon2',
            price=20,
            provider=provider,
            geojson="""{ "type": "Polygon", "coordinates":
            [ [ [ 2.319192095177777, 48.864936200483115 ],
            [ 2.320809898983764, 48.867157194778059 ], [ 2.340926937614733,
            48.860910397075138 ], [ 2.33973116958422, 48.859013067110759 ],
            [ 2.330165025340123, 48.86081784606256 ],
            [ 2.319192095177777, 48.864936200483115 ] ] ] }""",
        )

    def test_get_all_polygons(self):
        factory = APIRequestFactory()
        request = factory.get('/polygons/')
        view = PolygonViewSet.as_view({'get': 'list'})
        response = view(request)
        polygons = Polygon.objects.all()
        serializer = PolygonSerializer(polygons,
                                       many=True,
                                       context={'request': request}
                                      )
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class PolygonContainsPointTest(TestCase):
    """
    Test module for GET all polygons that contain a point API
    """
    def setUp(self):
        provider = Provider.objects.create(
            name='Provider1',
            email='email@example.com',
            phone='+77777777777',
            language='en',
            currency='USD',
            password='qwer1234',
        )
        # Place Concorde, Paris, contains the Luxor Obelisk point
        Polygon.objects.create(
            name='Place Concorde',
            price=10,
            provider=provider,
            geojson="""{ "type": "Polygon", "coordinates":
            [ [ [ 2.319192095177777, 48.864936200483115 ],
            [ 2.320809898983764, 48.867157194778059 ], [ 2.340926937614733,
            48.860910397075138 ], [ 2.33973116958422, 48.859013067110759 ],
            [ 2.330165025340123, 48.86081784606256 ],
            [ 2.319192095177777, 48.864936200483115 ] ] ] }""",
        )
        # Les Invalides, Paris, doesn't contain Luxor Obelisk point
        Polygon.objects.create(
            name='Les Invalides',
            price=20,
            provider=provider,
            geojson="""{ "type": "Polygon", "coordinates":
            [ [ [ 2.314620040943448, 48.853783518279236 ],
            [ 2.309600278334893, 48.853955228975558 ],
            [ 2.311173415443748, 48.862946406444827 ],
            [ 2.315182755310746, 48.862900209425625 ],
            [ 2.314620040943448, 48.853783518279236 ] ] ] }""",
        )

    def test_point_in_polygon(self):
        factory = APIRequestFactory()

        # The Luxor Obelisk Point
        point = """{ "type": "Point",
        "coordinates": [ 2.320880238279669, 48.865491458298109 ] }"""
        point_geojson = GEOSGeometry(point)
        request = factory.post('/points/',
                               json.dumps(point),
                               content_type='application/json',
                              )
        view = PointView.as_view()
        response = view(request)
        polygons = Polygon.objects.filter(geojson__contains=point_geojson)
        serializer = PolygonSerializer(polygons,
                                       many=True,
                                       context={'request': request}
                                      )
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
