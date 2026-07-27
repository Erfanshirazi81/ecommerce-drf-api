from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """Read-only: OrderItems are only ever created internally during checkout,
    never written directly by the client."""
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    """Read-only: an Order is only ever created via the checkout action,
    never via a plain POST with a client-supplied items list."""
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'items', 'total_price', 'status', 'created_at']
        read_only_fields = fields