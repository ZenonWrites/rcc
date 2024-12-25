from django.urls import path
from . import views

urlpatterns = [
    path('locations/', views.LocationViewSet.as_view({'get': 'list'}), name='location-list'),
    path('locations/<int:pk>/', views.LocationViewSet.as_view({'get': 'retrieve'}), name='location-detail'),
    path('locations/state/<str:state>/', views.LocationViewSet.as_view({'get': 'list'}), name='location-state'),
    path('locations/latlon/<str:lat>/<str:lon>/', views.LocationViewSet.as_view({'get': 'list'}), name='location-latlon'),
]