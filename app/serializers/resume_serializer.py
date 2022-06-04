from rest_framework import serializers
from ..models import ResumeData

# Default serializer
class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeData
        fields = '__all__'
