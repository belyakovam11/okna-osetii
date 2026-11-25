from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [ 'name', 'phone', 'address', 'comment', 'calculation', 'status', 'created_at'    ]
        read_only_fields = ['status','calculation']
