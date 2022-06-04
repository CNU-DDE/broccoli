from rest_framework import serializers
from ..models import ClaimData
from .user_serializer import UserDisplayNameSerializer

# Default serializer
class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimData
        fields = '__all__'

# Employer serializer
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
        resp["holder"] = UserDisplayNameSerializer(obj.owner).data
        return resp

# Employer serializer
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
