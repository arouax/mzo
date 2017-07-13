from .models import Provider, Polygon
from rest_framework import serializers


class PolygonSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Polygon
        fields = ('provider', 'name', 'price', 'geojson')


class ProviderSerializer(serializers.HyperlinkedModelSerializer):
    polygons = PolygonSerializer(source='polygon_set',
                                 many=True,
                                 read_only=True,
                                )

    def create(self, validated_data):
        provider = Provider(
            name=validated_data['name'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            language=validated_data['language'],
            currency=validated_data['currency'],
        )
        provider.set_password(validated_data['password'])
        provider.save()
        return provider

    class Meta:
        model = Provider
        fields = ('id', 'name', 'password', 'email', 'phone', 'language', 'currency', 'polygons')


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polygon
        fields = ('name', 'price', 'geojson')
