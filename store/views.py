from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from .models import Product, Variation, ReviewRating, ProductGallery
from .serializers import ProductSerializer, VariationSerializer, ReviewRatingSerializer, ProductGallerySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated, AllowAny

# ----------------- Products -----------------
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_name', 'category__name']
    ordering_fields = ['price', 'created_date', 'stock']
    ordering = ['-created_date']

    @swagger_auto_schema(
        operation_description="List all products with details, variations, reviews, and gallery.",
        tags=['Products']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve product details by slug.",
        tags=['Products'],
        responses={200: ProductSerializer}
    )
    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


# ----------------- Variations -----------------
class VariationListView(generics.ListAPIView):
    serializer_class = VariationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="List all variations (color, size) for a specific product.",
        tags=['Variations']
    )
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Variation.objects.filter(product_id=product_id)


# ----------------- Reviews -----------------
class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewRatingSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="List all reviews for a specific product.",
        tags=['Reviews']
    )
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ReviewRating.objects.filter(product_id=product_id, status=True)


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewRatingSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a review for a product (Authenticated user only).",
        tags=['Reviews'],
        security=[{'Bearer': []}],
        responses={201: ReviewRatingSerializer}
    )
    def post(self, request, product_id):
        serializer = ReviewRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product_id=product_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------- Product Gallery -----------------
class ProductGalleryView(generics.ListAPIView):
    serializer_class = ProductGallerySerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="List all gallery images for a specific product.",
        tags=['Gallery']
    )
    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductGallery.objects.filter(product_id=product_id)
