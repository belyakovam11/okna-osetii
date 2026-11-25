from rest_framework import serializers
from .models import ProfileSystem, WindowType, GlassUnit


class ProfileSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileSystem
        fields = ['id', 'name', 'slug', 'description', 'image']


class WindowTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WindowType
        fields = ['name','slug,']


class GlassUnitSerializer(serializers.ModelSerializer):
    class Meta: 
        model = GlassUnit
        fields = ['name','thickness','description']
