from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Order, OrderProduct
from .serializer import OrderSerializer

# ---------------- User Order Create ----------------
class UserOrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        order = Order.objects.create(
            user=request.user,
            first_name=request.user.first_name,
            last_name=request.user.last_name,
            email=request.user.email,
            phone=data.get('phone'),
            address_line_1=data.get('address_line_1'),
            address_line_2=data.get('address_line_2', ''),
            country=data.get('country'),
            state=data.get('state'),
            city=data.get('city'),
            order_note=data.get('order_note', ''),
            order_total=data.get('order_total'),
            tax=data.get('tax'),
        )

        # order products
        products = data.get('products', [])
        for p in products:
            product = OrderProduct.objects.create(
                order=order,
                user=request.user,
                product_id=p['product_id'],
                quantity=p['quantity'],
                product_price=p['product_price']
            )
            if 'variations' in p:
                product.variations.set(p['variations'])

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------- Delivery Man Orders List ----------------
class DeliveryManOrdersView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # শুধু assigned delivery man এর order দেখাবে
        orders = Order.objects.filter(assigned_delivery_man=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------- Update Order Status (Delivery Man) ----------------
class UpdateOrderStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, assigned_delivery_man=request.user)
        except Order.DoesNotExist:
            return Response({"error": "Order not found or not assigned to you"}, status=status.HTTP_404_NOT_FOUND)

        status_choice = request.data.get('status')
        if status_choice not in ['pending', 'assigned', 'delivered', 'completed']:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = status_choice
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
