from rest_framework import generics, permissions
from .models import Product, Variation, ReviewRating, ProductGallery
from .serializers import ProductSerializer, VariationSerializer, ReviewRatingSerializer, ProductGallerySerializer

# ---------------- Product Views ----------------
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAdminUser]

class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAdminUser]

# ---------------- Variation ----------------
class VariationListView(generics.ListAPIView):
    serializer_class = VariationSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Variation.objects.filter(product_id=product_id, is_active=True)

# ---------------- Review ----------------
class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product_id = self.kwargs['product_id']
        serializer.save(user=self.request.user, product_id=product_id)

class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewRatingSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ReviewRating.objects.filter(product_id=product_id, status=True)

# ---------------- Product Gallery ----------------
class ProductGalleryView(generics.ListCreateAPIView):
    serializer_class = ProductGallerySerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return ProductGallery.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs['product_id']
        serializer.save(product_id=product_id)
