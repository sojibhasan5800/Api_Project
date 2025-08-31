from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView,
    VariationListView, ReviewCreateView, ReviewListView, ProductGalleryView
)

urlpatterns = [
    # Product
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<slug:slug>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<slug:slug>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    # Variations
    path('products/<int:product_id>/variations/', VariationListView.as_view(), name='product-variations'),

    # Reviews
    path('products/<int:product_id>/reviews/', ReviewListView.as_view(), name='review-list'),
    path('products/<int:product_id>/reviews/create/', ReviewCreateView.as_view(), name='review-create'),

    # Product Gallery
    path('products/<int:product_id>/gallery/', ProductGalleryView.as_view(), name='product-gallery'),
]
