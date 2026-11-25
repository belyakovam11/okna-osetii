from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Post  # замените на реальное имя модели
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # TODO: настройте ordering / фильтрацию по опубликованным
   