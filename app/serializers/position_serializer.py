from rest_framework import serializers
from ..models import PositionData
from .user_serializer import UserDisplayNameSerializer, EmployerReadableSerializer

# Default serializer
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionData
        fields = '__all__'

# List serializer
class PositionListSerializer(serializers.ModelSerializer):

    # Serialize format
    class Meta:
        model = PositionData
        fields = [
            "id",
            "title",
            "employment_period",
            "working_time",
            "payment_interval_type",
            "payment_per_interval",
            "hiring_number",
        ]

    # Recursive formatting
    def to_representation(self, obj):
        resp = super().to_representation(obj)
        resp['employer'] = UserDisplayNameSerializer(obj.owner).data
        return resp

# Detail serializer
class PositionDetailSerializer(serializers.ModelSerializer):

    # Serialize format
    class Meta:
        model = PositionData
        fields = [
            "id",
            "title",
            "content",
            "employment_period",
            "working_time",
            "payment_interval_type",
            "payment_per_interval",
            "hiring_number",
        ]

    # Recursive formatting
    def to_representation(self, obj):
        resp = super().to_representation(obj)
        resp["employer"] = EmployerReadableSerializer(obj.owner).data
        return resp
