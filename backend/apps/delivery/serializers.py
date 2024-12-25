from rest_framework import serializers
from .models import DeliveryAssignment
from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer

class DeliveryAssignmentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), 
        source='order', 
        write_only=True
    )

    class Meta:
        model = DeliveryAssignment
        fields = [
            'id', 'order', 'order_id', 'delivery_agent', 
            'status', 'estimated_delivery_time', 
            'actual_delivery_time', 'delivery_notes'
        ]