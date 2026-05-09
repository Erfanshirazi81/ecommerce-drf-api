from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    AddToCartSerializer,
)

from products.models import Product


class CartViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    # GET /api/cart/
    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)

        serializer = CartSerializer(cart)

        return Response(serializer.data)

    # POST /api/cart/add/
    @action(detail=False, methods=["post"], serializer_class=AddToCartSerializer)
    def add(self, request):

        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
        )

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        cart_item.save()

        response_serializer = CartItemSerializer(cart_item)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    # PATCH /api/cart/item/{id}/
    @action(detail=True, methods=["patch"])
    def update_quantity(self, request, pk=None):

        try:
            cart_item = CartItem.objects.get(
                id=pk,
                cart__user=request.user
            )
        except CartItem.DoesNotExist:
            return Response(
                {"detail": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        quantity = request.data.get("quantity")

        if not quantity or int(quantity) < 1:
            return Response(
                {"detail": "Quantity must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartItemSerializer(cart_item)

        return Response(serializer.data)

    # DELETE /api/cart/item/{id}/
    @action(detail=True, methods=["delete"])
    def remove_item(self, request, pk=None):

        try:
            cart_item = CartItem.objects.get(
                id=pk,
                cart__user=request.user
            )
        except CartItem.DoesNotExist:
            return Response(
                {"detail": "Item not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_item.delete()

        return Response(
            {"detail": "Item removed from cart"},
            status=status.HTTP_204_NO_CONTENT
        )
