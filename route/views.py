import json

from django.contrib.gis.geos import LineString
from django.core.serializers import serialize
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Route


def display_route_map(request: HttpRequest, route_id: int) -> HttpResponse:
    """ Render route on the map """

    context = {}
    try:
        route = Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return HttpResponse("Route not found", status=404)

    context["route"] = json.loads(serialize("geojson", [route]))
    return render(request, 'map.html', context)


@require_http_methods(["GET"])
def get_route_by_id(request: HttpRequest, route_id: int) -> HttpResponse:
    try:
        route = Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return HttpResponse("Route not found", status=404)

    response = serialize('geojson', [route])
    return HttpResponse(response, content_type='application/json')


@require_http_methods(["POST"])
def create_route(request: HttpRequest) -> HttpResponse:

    body_data = json.loads(request.body.decode('utf-8'))
    route_name = body_data.get('name')
    route_coords = body_data.get('coordinates')

    segments = LineString(route_coords)
    route = Route(name=route_name, segments=segments)
    route.save()

    return HttpResponse(serialize('geojson', [route]), status=201)


@require_http_methods(["PUT"])
def update_route(request: HttpRequest, route_id: int) -> HttpResponse:
    try:
        route = Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return HttpResponse("Route not found", status=404)

    body_data = json.loads(request.body)
    route_name = body_data.get('name')
    route_coords = body_data.get('coordinates')

    route.name = route_name
    route.segments = LineString(route_coords)
    route.save()
    return HttpResponse(serialize('geojson', [route]), status=200)


@require_http_methods(["DELETE"])
def delete_route(request: HttpRequest, route_id: int) -> HttpResponse:
    try:
        route = Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return HttpResponse("Route not found", status=404)

    route.delete()
    return HttpResponse(status=204)
