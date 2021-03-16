from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from .models import Route


@admin.register(Route)
class RouteAdmin(OSMGeoAdmin):
    list_display = ('name', 'segments')
