from django.contrib.gis.db.models import LineStringField
from django.db import models


class Route(models.Model):
    """ Model representing bike route """

    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    segments = LineStringField(unique=True, null=False, blank=False)
