from ..models import CLData
from rest_framework import serializers

class CLSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLData
        fields = '__all__'
