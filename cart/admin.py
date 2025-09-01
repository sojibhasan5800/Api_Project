from django.contrib import admin
from .models import Cart, CartItem
from store.models import Product
from account.models import Account

# ---------------- CartItem Inline ----------------
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    readonly_fields = ('sub_total',)
    autocomplete_fields = ['product', 'user', 'cart']
    filter_horizontal = ('variations',)

# ---------------- Cart Admin ----------------
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added', 'total_items')
    search_fields = ('cart_id',)
    inlines = [CartItemInline]

    def total_items(self, obj):
        return obj.cartitem_set.count()
    total_items.short_description = "Total Items"

# ---------------- CartItem Admin ----------------
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'cart', 'quantity', 'is_active', 'sub_total')
    list_filter = ('is_active',)
    search_fields = ('product__product_name', 'user__email', 'cart__cart_id')
    autocomplete_fields = ['product', 'user', 'cart']
    filter_horizontal = ('variations',)
    readonly_fields = ('sub_total',)

# ---------------- Product Admin ----------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['product_name']


