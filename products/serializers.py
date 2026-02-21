from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['name', 'slug', 'description', 'price', 'stock', 'is_available', 'created_at', 'updated_at', 'category']
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']
        