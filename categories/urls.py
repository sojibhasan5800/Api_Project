from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet

router = DefaultRouter()
router.register('categories_api', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
 
]
