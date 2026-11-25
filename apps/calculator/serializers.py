from rest_framework import serializers
from .models import Calculation


class CalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculation
        fields = ['profile','window_type','glass','width','height','quantity','price','created_at']
