from rest_framework import viewsets, status # type: ignore
from rest_framework.decorators import action # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated # type: ignore
from rest_framework.authtoken.views import ObtainAuthToken # type: ignore
from django.http import JsonResponse
import requests
from .forms import AddressForm
from django.shortcuts import render
from geopy.geocoders import Nominatim
from .models import City, CustomUser, State, UserProfile, Address
from .serializers import (
    UserSerializer, UserUpdateSerializer,
    UserProfileSerializer, UserProfileUpdateSerializer,
    AddressSerializer , UserRegistrationSerializer,
    StateSerializer, CitySerializer, AreaSerializer,
)

class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['GET', 'PUT', 'PATCH'])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
            
        elif request.method in ['PUT', 'PATCH']:
            serializer = UserUpdateSerializer(
                user,
                data=request.data,
                partial=request.method == 'PATCH'
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'])
    def order_history(self, request):
        orders = request.user.orders.all().order_by('-created_at')
        from apps.orders.serializers import OrderSerializer
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def change_password(self, request):
        user = request.user
        if not user.check_password(request.data.get('old_password')):
            return Response(
                {'error': 'Invalid old password'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user.set_password(request.data.get('new_password'))
        user.save()
        return Response({'message': 'Password updated successfully'})


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response(UserRegistrationSerializer().data)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=400)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': UserSerializer(user).data,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user) # type: ignore
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'user_type': user.user_type
        })
    
class LocationViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['GET'])
    def states(self, request):
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def cities(self, request, pk=None):
        cities = City.objects.filter(state_id=pk)
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def areas(self, request, pk=None):
        areas = Area.objects.filter(city_id=pk)
        serializer = AreaSerializer(areas, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def get_location_details(self, request):
        """Get location details from coordinates"""
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        
        if not latitude or not longitude:
            return Response(
                {'error': 'Latitude and longitude are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Using Nominatim for reverse geocoding
        geolocator = Nominatim(user_agent="rcc_app")
        location = geolocator.reverse(f"{latitude}, {longitude}")
        
        if location and location.raw.get('address'):
            address = location.raw['address']
            
            # Find matching state and city from our database
            state = State.objects.filter(
                name__icontains=address.get('state', '')
            ).first()
            
            city = None
            if state:
                city = City.objects.filter(
                    state=state,
                    name__icontains=address.get('city', '')
                ).first()

            return Response({
                'state': StateSerializer(state).data if state else None,
                'city': CitySerializer(city).data if city else None,
                'pincode': address.get('postcode'),
                'raw_address': location.address
            })
            
        return Response(
            {'error': 'Location not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    @action(detail=False, methods=['POST'])
    def create_from_location(self, request):
        """Create address using current location"""
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        address_type = request.data.get('address_type', 'home')

        if not latitude or not longitude:
            return Response(
                {'error': 'Location coordinates are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get location details using the existing method
        location_viewset = LocationViewSet()
        location_response = location_viewset.get_location_details(request)
        
        if location_response.status_code != 200:
            return location_response

        location_data = location_response.data
        
        # Create address with the retrieved details
        address_data = {
            'user': request.user,
            'address_type': address_type,
            'state': location_data.get('state', {}).get('id'),
            'city': location_data.get('city', {}).get('id'),
            'pincode': location_data.get('pincode'),
            'latitude': latitude,
            'longitude': longitude,
            'street_address': location_data.get('raw_address', '')
        }

        serializer = self.get_serializer(data=address_data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def address_form_view(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            # Do something with the form data
            pass
    else:
        form = AddressForm()

    return render(request, 'address_form.html', {'form': form})

def cities_by_state(request):
    state_id = request.GET.get('state_id')
    cities = City.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)