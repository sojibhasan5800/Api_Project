from django.urls import path
from .views import UserOrderCreateView, DeliveryManOrdersView, UpdateOrderStatusView, PaymentListView

urlpatterns = [
    path('orders/create_api/', UserOrderCreateView.as_view(), name='user-order-create'),
    path('orders/delivery_api/', DeliveryManOrdersView.as_view(), name='delivery-orders'),
    path('orders/<int:pk>/update-status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
]
