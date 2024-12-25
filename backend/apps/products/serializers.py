from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source='category', 
        write_only=True
    )
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'category_id',
            'price', 'discount_price', 'discounted_price', 
            'image', 'weight', 'availability', 
            'is_featured', 'created_at', 'updated_at'
        ]

    def get_discounted_price(self, obj):
        return obj.discounted_price