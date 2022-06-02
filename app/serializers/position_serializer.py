from ..models import PositionData
from rest_framework import serializers

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionData
        fields = '__all__'
