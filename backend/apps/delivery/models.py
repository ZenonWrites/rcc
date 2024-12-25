from django.db import models
from apps.authentication.models import CustomUser
from apps.orders.models import Order

class DeliveryAssignment(models.Model):
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed', 'Delivery Failed')
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery')
    delivery_agent = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='deliveries'
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='assigned'
    )
    
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    actual_delivery_time = models.DateTimeField(null=True, blank=True)
    
    delivery_notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery for Order {self.order.id}"