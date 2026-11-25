from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Lead
from .serializers import LeadSerializer


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        # TODO: при необходимости фильтруйте по статусу через query-параметр ?status=new
        return qs
