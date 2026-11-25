from rest_framework import serializers
from .models import Service  # замените на реальное имя модели


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['name', 'slug', 'short_description', 'description', 'price', 'image', 'is_active', 'order', 'created_at', 'updated_at']
