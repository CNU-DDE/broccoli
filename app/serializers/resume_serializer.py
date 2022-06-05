from rest_framework import serializers
from ..models import ResumeData
from .user_serializer import UserDisplayNameSerializer

# Default serializer
class ResumeSerializer(serializers.ModelSerializer):

    # Serialized format
    class Meta:
        model = ResumeData
        fields = "__all__"

# Resume display format serializer
class ResumeDisplaySerializer(serializers.ModelSerializer):

    # Serialized format
    class Meta:
        model = ResumeData
        fields = [
            "id",
            "title",
        ]

    # Recursive formatting
    def to_representation(self, obj):
        resp = super().to_representation(obj)
        resp["holder"] = UserDisplayNameSerializer(obj.owner).data
        return resp
