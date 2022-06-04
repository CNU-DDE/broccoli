from rest_framework import serializers
from ..models import ClaimData
from . import user_serializer

# Default serializer
class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimData
        fields = '__all__'

# Claim list serializer for employer
class EmployerClaimListSerializer(serializers.ModelSerializer):

    # Serialize format
    class Meta:
        model = ClaimData
        fields = [
            "id",
            "title",
        ]

    # Recursive formatting
    def to_representation(self, obj):
        resp = super().to_representation(obj)
        resp["holder"] = user_serializer.UserDisplayNameSerializer(obj.owner).data
        return resp

# Claim list serializer for employee
class EmployeeClaimListSerializer(serializers.ModelSerializer):

    # Serialize format
    class Meta:
        model = ClaimData
        fields = [
            "id",
            "title",
        ]

    # Recursive formatting
    def to_representation(self, obj):
        resp = super().to_representation(obj)
        resp["issuer"] = UserDisplayNameSerializer(obj.owner).data
        return resp
