from django.urls import path, include
from rest_framework.routers import DefaultRouter # type: ignore
from .views import UserViewSet, AddressViewSet, CustomAuthToken, UserProfileViewSet, LocationViewSet
from rest_framework.authtoken.views import obtain_auth_token # type: ignore
from . import views

router = DefaultRouter()
router.register(r'location', LocationViewSet, basename='location')
router.register(r'users', UserViewSet, basename='user')
router.register(r'addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('profile/', UserViewSet.as_view({'get': 'profile'}), name='user-profile'),
    path('login/', CustomAuthToken.as_view(), name='api_login'),
    path('token/', obtain_auth_token, name='api_token'),
    path('me/', UserProfileViewSet.as_view({'get': 'me', 'put': 'me', 'patch': 'me'})),
    path('change-password/', UserProfileViewSet.as_view({'post': 'change_password'})),
    path('order-history/', UserProfileViewSet.as_view({'get': 'order_history'})),
    path('states/', LocationViewSet.as_view({'get': 'states'})),
    path('states/<int:pk>/cities/', LocationViewSet.as_view({'get': 'cities'})),
    path('cities/<int:pk>/areas/', LocationViewSet.as_view({'get': 'areas'})),
    path('get-location/', LocationViewSet.as_view({'post': 'get_location_details'})),
    path('address-from-location/', AddressViewSet.as_view({'post': 'create_from_location'})),
    path('address/', views.address_form_view, name='address_form'),
    path('cities_by_state/', views.cities_by_state, name='cities_by_state'),
]