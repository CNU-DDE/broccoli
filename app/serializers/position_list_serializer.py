from ..models import PositionData
from rest_framework import serializers

# Join & flatten instance
# Ref: https://stackoverflow.com/a/48722394
class PositionListSerializer(serializers.ModelSerializer):

    owner_display_name = serializers.SerializerMethodField()

    class Meta:
        model = PositionData
        fields = [
            "id",
            "title",
            "owner_display_name",
            "employment_period",
            "working_time",
            "payment_interval_type",
            "payment_per_interval",
            "hiring_number",
        ]

    def get_owner_display_name(self, obj):
        return obj.owner.display_name
