from ..models import CLData
from rest_framework import serializers

class CLListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLData
        fields = ["id", "title", "content"]
