
from rest_framework import serializers
from .models import GalleryItem  # замените на реальное имя модели


class GalleryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryItem
        fields = [ "slug", 'name',  'price', 'rub', 'in_stock',]
