from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery

# ---------------- Product Admin ----------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'price', 'stock', 'is_available', 'created_date', 'modified_date')
    list_filter = ('category', 'is_available', 'created_date')
    search_fields = ('product_name', 'description')
    prepopulated_fields = {'slug': ('product_name',)}
    list_editable = ('price', 'stock', 'is_available')
    readonly_fields = ('created_date', 'modified_date')
    ordering = ('-created_date',)


# ---------------- Variation Admin ----------------
@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date')
    list_filter = ('variation_category', 'is_active', 'created_date')
    search_fields = ('variation_value', 'product__product_name')
    ordering = ('-created_date',)


# ---------------- Review Rating Admin ----------------
@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'subject', 'rating', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'rating', 'created_at')
    search_fields = ('subject', 'review', 'user__email', 'product__product_name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


# ---------------- Product Gallery Admin ----------------
@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product__product_name',)
