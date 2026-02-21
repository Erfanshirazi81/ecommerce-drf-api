from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def list(self, request):
        ser_data = CategorySerializer(instance = self.queryset, many = True).data
        return Response(ser_data)

class ProductsViewSet(viewsets.ViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def list(self, request):
        ser_data = ProductSerializer(instance = self.queryset, many = True).data
        return Response(ser_data)
        