from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    VariationListView, ReviewCreateView, ReviewListView, ProductGalleryView
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:product_id>/variations/', VariationListView.as_view(), name='product-variations'),
    path('products/<int:product_id>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('products/<int:product_id>/reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('products/<int:product_id>/gallery/', ProductGalleryView.as_view(), name='product-gallery'),
]
