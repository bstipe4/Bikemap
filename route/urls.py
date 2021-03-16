from django.urls import path

from . import views

urlpatterns = [
    path('map/<str:route_id>', views.display_route_map, name='show-map'),
    path('api/route/<str:route_id>', views.get_route_by_id, name='get-route'),
    path('api/route', views.create_route, name='create-route'),
    path('api/route/<str:route_id>/update', views.update_route, name='update-route'),
    path('api/route/<str:route_id>/delete', views.delete_route, name='delete-route'),
]
