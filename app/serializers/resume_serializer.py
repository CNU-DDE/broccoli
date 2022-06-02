from ..models import ResumeData
from rest_framework import serializers

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeData
        fields = '__all__'
