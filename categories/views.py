from rest_framework import viewsets, permissions
from .models import Category
from .serializers import CategorySerializer
from django.http import HttpResponse, JsonResponse
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]  
    lookup_field = 'pk' 
