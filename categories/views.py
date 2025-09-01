from rest_framework import viewsets, permissions
from .models import Category
from .serializers import CategorySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Category Management API
    """
    
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]  
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_summary="List all categories",
        operation_description="Retrieve a list of all categories with their details.",
        tags=["Categories"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve category by ID",
        operation_description="Get details of a single category using its ID.",
        tags=["Categories"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new category",
        operation_description="Add a new category to the system. Admin access recommended.",
        tags=["Categories"],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update an existing category",
        operation_description="Update category details using its ID. Partial update supported with PATCH.",
        tags=["Categories"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial update category",
        operation_description="Update one or more fields of a category using its ID.",
        tags=["Categories"],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a category",
        operation_description="Remove a category from the system using its ID.",
        tags=["Categories"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
