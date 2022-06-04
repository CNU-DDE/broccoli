from ..models import PositionData, User
from rest_framework import serializers

# Django ORM supports limited table joining
# Ref: https://stackoverflow.com/a/43198182
class UserDisplaynameOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["display_name"]

class PositionListSerializer(serializers.ModelSerializer):
    owner = UserDisplaynameOnlySerializer(read_only=True)

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
