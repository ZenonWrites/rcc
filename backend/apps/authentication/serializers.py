from rest_framework import serializers
from .models import CustomUser, UserProfile, Address, State, City, Area

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name', 'code']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'is_urban', 'state']

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name', 'pincode', 'city', 'latitude', 'longitude']

class AddressSerializer(serializers.ModelSerializer):
    state_details = StateSerializer(source='state', read_only=True)
    city_details = CitySerializer(source='city', read_only=True)
    area_details = AreaSerializer(source='area', read_only=True)

    class Meta:
        model = Address
        fields = [
            'id', 'address_type', 'state', 'state_details',
            'city', 'city_details', 'area', 'area_details',
            'street_address', 'landmark', 'pincode',
            'is_primary', 'latitude', 'longitude'
        ]
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id', 'alternate_phone', 'emergency_contact',
            'default_address', 'preferred_delivery_time',
            'vehicle_number', 'vehicle_type', 'loyalty_points',
            'member_since'
        ]

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'alternate_phone', 'emergency_contact',
            'preferred_delivery_time'
        ]

class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'phone_number',
            'user_type', 'profile_picture', 'date_of_birth',
            'gender', 'notification_enabled', 'email_notifications',
            'whatsapp_notifications', 'preferred_language',
            'addresses', 'profile'
        ]
        read_only_fields = ['id', 'user_type']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'email', 'profile_picture', 'date_of_birth',
            'gender', 'notification_enabled', 'email_notifications',
            'whatsapp_notifications', 'preferred_language'
        ]

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'email', 'password', 'profile_picture']
        extra_kwargs = {
            'email': {'required': True},
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        user.user_type = 'customer'  # Ensure the user is always a customer
        user.save()
        return user