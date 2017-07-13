"""
mzo_project URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from providers import views

router = routers.DefaultRouter()
router.register(r'providers', views.ProviderViewSet)
router.register(r'polygons', views.PolygonViewSet)


schema_view = get_schema_view(
    title='Providers API',
    renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    url(r'^providers/get-by-point/$', views.PointView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-docs/$', schema_view, name="docs"),
]
