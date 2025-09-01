from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve current user's cart with all active items",
        responses={200: CartSerializer},
        security=[{'Bearer': []}]
    )
    def list(self, request):
        cart, created = Cart.objects.get_or_create(cart_id=str(request.user.id))
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=CartItemSerializer,
        operation_description="Add a product to the current user's cart with optional variations",
        responses={201: CartItemSerializer, 400: "Validation Error"},
        security=[{'Bearer': []}]
    )
    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(cart_id=str(request.user.id))
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Remove an item from cart (soft delete)",
        responses={200: "Item removed successfully", 404: "Item not found"},
        manual_parameters=[openapi.Parameter('pk', openapi.IN_PATH, description="CartItem ID", type=openapi.TYPE_INTEGER)],
        security=[{'Bearer': []}]
    )
    def remove_item(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(id=pk, user=request.user)
            cart_item.is_active = False
            cart_item.save()
            return Response({"message": "Item removed successfully"}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['quantity'],
            properties={
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='New quantity for the cart item')
            }
        ),
        operation_description="Update quantity of an existing cart item",
        responses={200: CartItemSerializer, 400: "Invalid quantity", 404: "Item not found"},
        manual_parameters=[openapi.Parameter('pk', openapi.IN_PATH, description="CartItem ID", type=openapi.TYPE_INTEGER)],
        security=[{'Bearer': []}]
    )
    def update_quantity(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(id=pk, user=request.user)
            quantity = request.data.get('quantity')
            if quantity and int(quantity) > 0:
                cart_item.quantity = int(quantity)
                cart_item.save()
                return Response(CartItemSerializer(cart_item).data, status=status.HTTP_200_OK)
            return Response({"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
