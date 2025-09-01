from django.contrib import admin
from .models import Payment, Order, OrderProduct

# ---------------- Payment Admin ----------------
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'payment_method', 'amount_paid', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('payment_id', 'user__email', 'payment_method')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

# ---------------- Order Product Inline ----------------
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('user', 'product', 'product_price', 'quantity', 'ordered')
    can_delete = False

# ---------------- Order Admin ----------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'assigned_delivery_man', 'status', 'order_total', 'is_ordered', 'created_at')
    list_filter = ('status', 'is_ordered', 'created_at', 'assigned_delivery_man')
    search_fields = ('order_number', 'user__email', 'first_name', 'last_name', 'email', 'phone')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'order_total', 'tax', 'delivery_fee')
    ordering = ('-created_at',)
    inlines = [OrderProductInline]

# ---------------- OrderProduct Admin ----------------
@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'user', 'quantity', 'product_price', 'ordered', 'created_at')
    list_filter = ('ordered', 'created_at')
    search_fields = ('product__product_name', 'order__order_number', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
