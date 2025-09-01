from rest_framework import serializers
from .models import Cart, CartItem
from store.models import Product, Variation
from account.models import Account

# Product Serializer (simple)
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'description']
        ref_name = 'CartProductSerializer'

# Variation Serializer
class VariationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='variation_category', read_only=True)
    value = serializers.CharField(source='variation_value', read_only=True)
    class Meta:
        model = Variation
        fields = ['id', 'name', 'value']
        ref_name = 'CartVariationSerializer' 

# CartItem Serializer
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variations = VariationSerializer(many=True, read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source='product'
    )
    variation_ids = serializers.PrimaryKeyRelatedField(
        queryset=Variation.objects.all(), many=True, write_only=True, source='variations', required=False
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'variations', 'product_id', 'variation_ids', 'quantity', 'sub_total', 'is_active']

    def create(self, validated_data):
        variations = validated_data.pop('variations', [])
        cart_item = CartItem.objects.create(**validated_data)
        cart_item.variations.set(variations)
        return cart_item

# Cart Serializer
class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'cart_id', 'date_added', 'items', 'total_price']

    def get_items(self, obj):
        items = CartItem.objects.filter(cart=obj, is_active=True)
        return CartItemSerializer(items, many=True).data

    def get_total_price(self, obj):
        items = CartItem.objects.filter(cart=obj, is_active=True)
        total = sum([item.sub_total() for item in items])
        return total
