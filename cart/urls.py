from django.urls import path
from .views import CartViewSet

cart_list = CartViewSet.as_view({'get': 'list'})
add_item = CartViewSet.as_view({'post': 'add_item'})
remove_item = CartViewSet.as_view({'delete': 'remove_item'})
update_quantity = CartViewSet.as_view({'patch': 'update_quantity'})

urlpatterns = [
    path('cart/', cart_list, name='cart-list'),
    path('cart/add/', add_item, name='cart-add-item'),
    path('cart/remove/<int:pk>/', remove_item, name='cart-remove-item'),
    path('cart/update/<int:pk>/', update_quantity, name='cart-update-quantity'),
]
