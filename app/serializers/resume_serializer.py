from rest_framework import serializers

from . import user_serializer
from ..models import ResumeData

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
        resp["holder"] = user_serializer.UserDisplayNameSerializer(obj.owner).data
        if obj.verifier:
            resp["verifier"] = user_serializer.UserDisplayNameSerializer(obj.verifier).data
        else:
            resp["verifier"] = None
        return resp

class ResumeDetailSerializer(serializers.ModelSerializer):

    #Serialized format
    class Meta:
        model = ResumeData
        fields = [
            "id",
            "title",
            "position",
        ]

    # Recursive formatting
    def to_representation(self, obj):
        resp = super().to_representation(obj)

        # Format holder
        resp["holder"] = user_serializer.EmployeeReadableSerializer(obj.owner).data

        # Format verifier
        if obj.verifier:
            resp["verifier"] = user_serializer.EmployerReadableSerializer(obj.verifier).data
        else:
            resp["verifier"] = None

        # Save cover letter list to process on view-level
        resp["cover_letters"] = obj.content["cover_letters"]

        # Save VP to process on view-level
        resp["careers"] = obj.content["careers"]

        return resp
