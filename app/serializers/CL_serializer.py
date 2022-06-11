from ..models import CLData
from rest_framework import serializers

# Default serializer
class CLSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLData
        fields = '__all__'

# CL minimum serializer
class CLMinimumSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLData
        fields = (
            "id",
            "owner",
            "title",
        )

# CL detail serializer
class CLDetailSerializer(CLMinimumSerializer):
    class Meta:
        model = CLData
        fields = CLMinimumSerializer.Meta.fields + (
            "content",
        )
