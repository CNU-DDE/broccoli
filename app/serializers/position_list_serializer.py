from ..models import PositionData
from rest_framework import serializers

class PositionListSerializer(serializers.ModelSerializer):

    # JOIN field
    employer_display_name = serializers.SerializerMethodField()

    # Serialize format
    class Meta:
        model = PositionData
        fields = [
            "id",
            "title",
            "employer_display_name",
            "employment_period",
            "working_time",
            "payment_interval_type",
            "payment_per_interval",
            "hiring_number",
        ]

    # JOIN path
    def get_employer_display_name(self, obj):
        return obj.owner.display_name
