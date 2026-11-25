from rest_framework import viewsets
from .models import ProfileSystem, WindowType, GlassUnit
from .serializers import (
    ProfileSystemSerializer,
    WindowTypeSerializer,
    GlassUnitSerializer,
)


class ProfileSystemViewSet(viewsets.ModelViewSet):
    queryset = ProfileSystem.objects.all()
    serializer_class = ProfileSystemSerializer


class WindowTypeViewSet(viewsets.ModelViewSet):
    queryset = WindowType.objects.all()
    serializer_class = WindowTypeSerializer
    # TODO: при необходимости добавьте permission_classes / filter_backends


class GlassUnitViewSet(viewsets.ModelViewSet):
    queryset = GlassUnit.objects.all()
    serializer_class = GlassUnitSerializer
    # TODO: при необходимости добавьте permission_classes / filter_backends

