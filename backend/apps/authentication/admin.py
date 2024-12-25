from django.contrib import admin
from .models import CustomUser, Address

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'user_type')
    list_filter = ('user_type',)
    search_fields = ('username', 'email', 'phone_number')

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'city', 'state', 'pincode', 'is_primary')
    list_filter = ('city', 'state', 'is_primary')
    search_fields = ('user__username', 'street_address', 'city', 'state', 'pincode')
