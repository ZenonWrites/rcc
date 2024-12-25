from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    AVAILABILITY_CHOICES = [
        ('in_stock', 'In Stock'),
        ('limited', 'Limited Stock'),
        ('out_of_stock', 'Out of Stock')
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/')
    weight = models.FloatField(help_text='Weight in grams')
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='in_stock')
    
    is_featured = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        return self.discount_price or self.price