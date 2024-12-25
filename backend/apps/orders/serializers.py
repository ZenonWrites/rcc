from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.models import Product
from apps.products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), 
        source='product', 
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'total_amount', 'status', 
            'payment_method', 'created_at', 'updated_at', 
            'items'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        total_amount = 0
        for item_data in items_data:
            item = OrderItem.objects.create(
                order=order, 
                product=item_data['product'], 
                quantity=item_data['quantity'], 
                price=item_data['product'].price
            )
            total_amount += item.total_price()
        
        order.total_amount = total_amount
        order.save()
        
        return order