from rest_framework import serializers
from .models import Post  # замените на реальное имя модели


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            # TODO: укажите поля модели
        ]
