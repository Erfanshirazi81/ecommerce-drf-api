from rest_framework import serializers  
from .models import Order, OrderItem    
from django.db import transaction

class OrderItemSerializer(serializers.ModelSerializer): 
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "items", "total_price", "status", "created_at"]
        read_only_fields = ["total_price", "status", "created_at"]
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
    
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            total_price = 0 
            for item in items_data:
                product = item['product']
                quantity = item['quantity']
                
                if product.stock < quantity:
                    raise serializers.ValidationError(f"Not enough stock for {product.name}. Available: {product.stock}")
                
                product.stock -= quantity
                product.save()

                price = product.price * quantity
                total_price += price
                OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
            order.total_price = total_price
            order.save()
        return order
    