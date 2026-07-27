from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import Cart
from products.models import Product
from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    """
    Orders are only ever created through checkout(), never through a plain
    POST/PUT/PATCH/DELETE — that's why this uses GenericViewSet + the two
    read-only mixins instead of ModelViewSet. A user can list and view their
    own orders, and nothing else.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_items = list(cart.items.select_related('product'))

        if not cart_items:
            return Response(
                {'detail': 'Your cart is empty.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            # select_for_update() locks these product rows until the
            # transaction ends, so two simultaneous checkouts can't both
            # oversell the same last unit of stock.
            product_ids = [item.product_id for item in cart_items]
            locked_products = Product.objects.select_for_update().in_bulk(product_ids)

            for item in cart_items:
                product = locked_products[item.product_id]
                if product.stock < item.quantity:
                    return Response(
                        {'detail': f"Not enough stock for '{product.name}'. Available: {product.stock}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            order = Order.objects.create(user=request.user)
            total_price = 0
            for item in cart_items:
                product = locked_products[item.product_id]
                product.stock -= item.quantity
                product.save()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    price=product.price,
                )
                total_price += product.price * item.quantity

            order.total_price = total_price
            order.save()

            cart.items.all().delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)