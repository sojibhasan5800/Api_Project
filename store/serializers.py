from rest_framework import serializers
from .models import Product, Variation, ReviewRating, ProductGallery

# ---------------- Product Gallery ----------------
class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = ['id', 'image']

# ---------------- Variation ----------------
class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ['id', 'variation_category', 'variation_value', 'is_active']
        # ref_name = 'StoreVariationSerializers'
        ref_name = 'StoreVariationSerializer'

# ---------------- Review ----------------
class ReviewRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # shows user email

    class Meta:
        model = ReviewRating
        fields = ['id', 'user', 'subject', 'review', 'rating', 'status', 'created_at']

# ---------------- Product ----------------
class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    variations = VariationSerializer(source='variation_set', many=True, read_only=True)
    reviews = ReviewRatingSerializer(source='reviewrating_set', many=True, read_only=True)
    gallery = ProductGallerySerializer(source='productgallery_set', many=True, read_only=True)
    average_rating = serializers.FloatField(source='averageReview', read_only=True)
    review_count = serializers.IntegerField(source='countReview', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'slug', 'description', 'price', 'images', 
            'stock', 'is_available', 'category', 'created_date', 'modified_date',
            'average_rating', 'review_count', 'variations', 'reviews', 'gallery'
        ]
        ref_name = 'StoreProductSerializer'
