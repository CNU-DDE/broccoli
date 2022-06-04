from ..models import CLData
from rest_framework import serializers

# Default serializer
class CLSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLData
        fields = '__all__'

# List serializer
class CLListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLData
        fields = ["id", "title", "content"]
