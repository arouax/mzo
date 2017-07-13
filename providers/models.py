from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.gis.db.models import PolygonField
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.
class Provider(AbstractBaseUser):
    """
    A model that defines providers.
    """
    name = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    phone = PhoneNumberField()
    language = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)

    USERNAME_FIELD = 'name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'phone', 'language', 'currency']


    def __str__(self):
        return self.name


class Polygon(models.Model):
    """
    A model that defines a polygon with a foreign key to Provider.
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Service Area Name',
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey('Provider', on_delete=models.CASCADE)
    geojson = PolygonField(verbose_name='Coordinates')

    def __str__(self):
        return self.name
