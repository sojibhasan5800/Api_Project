from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart, created = Cart.objects.get_or_create(cart_id=str(request.user.id))
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(cart_id=str(request.user.id))
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, cart=cart)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def remove_item(self, request, pk=None):
        try:
            cart_item = CartItem.objects.get(id=pk, user=request.user)
            cart_item.is_active = False
            cart_item.save()
            return Response({"message": "Item removed successfully"}, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

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
