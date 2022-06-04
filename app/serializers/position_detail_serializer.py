from ..models import PositionData
from rest_framework import serializers

class PositionDetailSerializer(serializers.ModelSerializer):

    # JOIN fields
    employer_display_name = serializers.SerializerMethodField()
    employer_contact = serializers.SerializerMethodField()
    employer_email = serializers.SerializerMethodField()
    employer_address = serializers.SerializerMethodField()

    # Serialize format
    class Meta:
        model = PositionData
        fields = [
            "id",
            "title",
            "content",
            "employer_display_name",
            "employer_contact",
            "employer_email",
            "employer_address",
            "employment_period",
            "working_time",
            "payment_interval_type",
            "payment_per_interval",
            "hiring_number",
        ]

    # JOIN paths
    def get_employer_display_name(self, obj):
        return obj.owner.display_name

    def get_employer_contact(self, obj):
        return obj.owner.contact

    def get_employer_email(self, obj):
        return obj.owner.email

    def get_employer_address(self, obj):
        return obj.owner.address
