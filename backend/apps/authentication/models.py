from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('owner', 'Owner'),
        ('admin', 'Admin/Manager'),
        ('delivery', 'Delivery Agent'),
        ('customer', 'Customer')
    )

    phone_number = models.CharField(max_length=15, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    # Location details for delivery agents and customers
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], null=True, blank=True)
    
    # Preferences
    notification_enabled = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    whatsapp_notifications = models.BooleanField(default=False)
    preferred_language = models.CharField(
        max_length=10,
        choices=[('en', 'English'), ('hi', 'Hindi')],
        default='en'
    )
    
    def __str__(self):
        return f"{self.username} - {self.user_type}"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    
    # Additional contact info
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    
    # Delivery preferences
    default_address = models.ForeignKey(
        'Address', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='default_for_profiles'
    )
    preferred_delivery_time = models.CharField(
        max_length=20,
        choices=[
            ('morning', '9 AM - 12 PM'),
            ('afternoon', '12 PM - 3 PM'),
            ('evening', '3 PM - 6 PM'),
            ('night', '6 PM - 9 PM')
        ],
        default='evening'
    )
    
    # For delivery agents
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    vehicle_type = models.CharField(
        max_length=20,
        choices=[
            ('bike', 'Bike'),
            ('scooter', 'Scooter'),
            ('cycle', 'Cycle')
        ],
        blank=True,
        null=True
    )
    
    # Loyalty program
    loyalty_points = models.IntegerField(default=0)
    member_since = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

class State(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)  # For state codes like MH, KA, etc.

    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)
    is_urban = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}, {self.state.name}"

class Area(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='areas')
    name = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    
    # Coordinates for the area
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.name}, {self.city.name}"

# Modified Address model
class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(
        max_length=20,
        choices=[
            ('home', 'Home'),
            ('work', 'Work'),
            ('other', 'Other')
        ],
        default='home'
    )
    
    # Location hierarchy
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    
    street_address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10)
    is_primary = models.BooleanField(default=False)
    
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)