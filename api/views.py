from django.shortcuts import render
from rest_framework import generics,mixins
from blog.models import Blog,Comment
from blog.serializers import BlogSerializer,CommentSerializer

# Create your views here.
class BlogsView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
  

class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer