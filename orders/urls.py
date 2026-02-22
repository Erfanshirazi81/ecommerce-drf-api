from django.urls import path
from . import views 
from rest_framework import routers  


app_name = 'orders'
urlpatterns = [

]

routers = routers.SimpleRouter()
routers.register('orders', views.OrderViewSet, basename='orders')
urlpatterns += routers.urls

