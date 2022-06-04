from ..models import ClaimData
from rest_framework import serializers

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimData
        fields = '__all__'
