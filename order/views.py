from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Order, OrderProduct, Payment
from .serializer import OrderSerializer, OrderProductSerializer, PaymentSerializer

# ------------------- User Order Create -------------------
class UserOrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=OrderSerializer,
        responses={201: OrderSerializer},
        operation_description="Create a new order for logged-in user",
        operation_summary="Create User Order",
        tags=['Order Management']
    )
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Order created successfully", "order": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ------------------- Delivery Man Orders -------------------
class DeliveryManOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: OrderSerializer(many=True)},
        operation_description="Get all orders assigned to the logged-in delivery man",
        operation_summary="Assigned Orders for Delivery Man",
        tags=['Order Management']
    )
    def get(self, request):
        orders = Order.objects.filter(assigned_delivery_man=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ------------------- Update Order Status -------------------
class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    status_param = openapi.Parameter(
        'status', openapi.IN_QUERY, description="New status for the order",
        type=openapi.TYPE_STRING, required=True, enum=['pending', 'assigned', 'delivered', 'completed']
    )

    @swagger_auto_schema(
        manual_parameters=[status_param],
        responses={200: OrderSerializer, 400: "Invalid status"},
        operation_description="Update the status of an order",
        operation_summary="Update Order Status",
        tags=['Order Management']
    )
    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.query_params.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save()
        serializer = OrderSerializer(order)
        return Response({"message": "Order status updated successfully", "order": serializer.data}, status=status.HTTP_200_OK)


# ------------------- Payment Details -------------------
class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all().order_by('-created_at')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    swagger_tags = ['Payment Management']
