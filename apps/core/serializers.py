
from rest_framework import serializers


# В приложении core обычно нет собственных моделей,
# но можно разместить здесь общие/служебные сериализаторы.

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    message = serializers.CharField(required=False, allow_blank=True)
