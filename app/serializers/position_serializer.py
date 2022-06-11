from rest_framework import serializers
from ..models import PositionData
from .user_serializer import UserMinimumSerializer, EmployerReadableSerializer

# Default serializer
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PositionData
        fields = '__all__'

# Minimum position info serializer
class PositionMinimumSerializer(serializers.ModelSerializer):

    # Serialize format
    class Meta:
        model = PositionData
        fields = (
            "id",
            "title",
            "employment_period",
            "working_time",
            "payment_interval_type",
            "payment_per_interval",
            "hiring_number",
        )

    # Recursive formatting
    def to_representation(self, obj):
        resp = super().to_representation(obj)
        resp['employer'] = UserMinimumSerializer(obj.owner).data
        return resp

# Detail serializer
class PositionDetailSerializer(PositionMinimumSerializer):

    # Serialize format
    class Meta:
        model = PositionData
        fields = PositionMinimumSerializer.Meta.fields + (
            "content",
        )

    # Recursive formatting
    # @override
    def to_representation(self, obj):
        resp = super().to_representation(obj)
        resp["employer"] = EmployerReadableSerializer(obj.owner).data
        return resp
