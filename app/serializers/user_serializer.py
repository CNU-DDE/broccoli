from django.contrib.auth import get_user_model
from rest_framework import serializers

# Default serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

# Display name only serializer
class UserDisplayNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["display_name"]

# Human readable serializer for employer
class EmployerReadableSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "display_name",
            "contact",
            "email",
            "address",
        ]

# Human readable serializer for employee
class EmployeeReadableSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "display_name",
            "contact",
            "email",
            "address",
            "birth",
        ]
