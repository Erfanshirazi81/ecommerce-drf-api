from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductCreateUpdateSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_serializer_class(self):
        return CategorySerializer


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProductCreateUpdateSerializer
        return super().get_serializer_class()     
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny, ]
        else:
            permission_classes = [IsAdminUser, ]
        
        return [permission() for permission in permission_classes]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_available']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['created_at']
    