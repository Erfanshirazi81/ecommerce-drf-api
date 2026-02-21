from django.urls import path
from . import views
from rest_framework import routers

app_name = 'products'
urlpatterns = [
    
]

routers = routers.SimpleRouter()
routers.register('categorys', views.CategoryViewSet, basename='categorys')
routers.register('products', views.ProductsViewSet, basename='products')

urlpatterns += routers.urls