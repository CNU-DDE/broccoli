from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import PositionData

# Nested serializer
class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "display_name",
            "contact",
            "email",
            "address",
        ]

# Main serializer
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
        resp["employer"] = EmployerSerializer(obj.owner).data
        return resp
