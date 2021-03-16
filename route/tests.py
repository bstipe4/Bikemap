import ast

import pytest
from django.db import IntegrityError
from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from .models import Route


@pytest.mark.django_db(reset_sequences=True)
@pytest.fixture
def existing_route(client: Client) -> Route:
    response = create_route(client)
    created_route_id = get_route_id_from_response(response)
    return Route.objects.get(id=created_route_id)


def get_route_id_from_response(response: HttpResponse) -> str:
    resp_dict = ast.literal_eval(response.content.decode('utf-8'))
    created_route_id = resp_dict['features'][0]['properties']['pk']
    return created_route_id


def get_route_name_from_response(response: HttpResponse) -> str:
    resp_dict = ast.literal_eval(response.content.decode('utf-8'))
    created_route_name = resp_dict['features'][0]['properties']['name']
    return created_route_name


def create_route(client: Client) -> HttpResponse:
    create_route_url = reverse('create-route')
    data = {
        "name": "test route",
        "coordinates": [
            [16.482415793036196, 43.52003298156595],
            [16.486642954442942, 43.52194679186345]
        ]
    }
    response = client.post(create_route_url, data=data, content_type="application/json")
    return response


@pytest.mark.django_db(reset_sequences=True)
def test_non_existing_route_rendered(client):
    display_map_url = reverse('show-map', kwargs={'route_id': 1})
    response = client.get(display_map_url)
    assert response.status_code == 404


@pytest.mark.django_db(reset_sequences=True)
def test_existing_route_rendered(client, existing_route):

    display_map_url = reverse('show-map', kwargs={'route_id': existing_route.id})
    response = client.get(display_map_url)

    assertTemplateUsed(response, 'map.html')
    assert response.status_code == 200


@pytest.mark.django_db(reset_sequences=True)
def test_creating_route(client):
    response = create_route(client)

    assert response.status_code == 201
    assert Route.objects.get(name=get_route_name_from_response(response))


@pytest.mark.django_db(reset_sequences=True)
def test_creating_routes_with_same_name(client):
    create_route(client)
    with pytest.raises(IntegrityError):
        create_route(client)


@pytest.mark.django_db(reset_sequences=True)
def test_get_non_existing_route_by_id(client):
    get_route_url = reverse('get-route', kwargs={'route_id': 1})
    response = client.get(get_route_url)

    assert response.status_code == 404


@pytest.mark.django_db(reset_sequences=True)
def test_get_existing_route_by_id(client, existing_route):
    get_route_url = reverse('get-route', kwargs={'route_id': existing_route.id})
    response = client.get(get_route_url)

    assert response.status_code == 200


@pytest.mark.django_db(reset_sequences=True)
def test_update_non_existing_route(client):
    update_route_url = reverse('update-route', kwargs={'route_id': 1})
    data = {
        "name": "test route 2",
        "coordinates": [
            [16.0, 43.52003298156595],
            [16.486642954442942, 43.52194679186345]
        ]
    }
    response = client.put(update_route_url, data=data, content_type="application/json")

    assert response.status_code == 404


@pytest.mark.django_db(reset_sequences=True)
def test_update_existing_route(client, existing_route):
    updated_route_name = "test route 2"

    update_route_url = reverse('update-route', kwargs={'route_id': existing_route.id})
    data = {
        "name": updated_route_name,
        "coordinates": [
            [16.0, 43.52003298156595],
            [16.486642954442942, 43.52194679186345]
        ]
    }
    response = client.put(update_route_url, data=data, content_type="application/json")

    assert response.status_code == 200

    updated_route = Route.objects.get(id=existing_route.id)
    assert updated_route.name == updated_route_name
    assert updated_route.segments[0][0] == 16.0


@pytest.mark.django_db(reset_sequences=True)
def test_delete_non_existing_route(client):
    delete_route_url = reverse('delete-route', kwargs={'route_id': 1})
    response = client.delete(delete_route_url)
    assert response.status_code == 404


@pytest.mark.django_db(reset_sequences=True)
def test_delete_existing_route(client, existing_route):

    delete_route_url = reverse('delete-route', kwargs={'route_id': existing_route.id})
    response = client.delete(delete_route_url)
    assert response.status_code == 204

    with pytest.raises(Route.DoesNotExist):
        Route.objects.get(id=existing_route.id)
