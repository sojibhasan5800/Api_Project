from rest_framework import serializers
from .models import Order, OrderProduct, Payment
from account.models import Account
from store.models import Product, Variation

# ---------------- Payment Serializer ----------------
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_id', 'payment_method', 'amount_paid', 'status', 'created_at']

# ---------------- OrderProduct Serializer ----------------
class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.product_name')
    variations = serializers.StringRelatedField(many=True)

    class Meta:
        model = OrderProduct
        fields = ['id', 'product', 'product_name', 'variations', 'quantity', 'product_price', 'ordered', 'created_at', 'updated_at']

# ---------------- User Order Serializer ----------------
class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(source='orderproduct_set', many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)
    user_email = serializers.ReadOnlyField(source='user.email')
    assigned_delivery_man = serializers.ReadOnlyField(source='assigned_delivery_man.username')

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_email', 'payment', 'order_number', 'first_name', 'last_name', 'phone', 'email',
            'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note', 'order_total', 'tax',
            'status', 'assigned_delivery_man', 'ip', 'is_ordered', 'created_at', 'updated_at', 'order_products'
        ]
        read_only_fields = ['order_number', 'status', 'is_ordered', 'created_at', 'updated_at']
