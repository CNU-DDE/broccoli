from django.contrib.auth import get_user_model
from rest_framework import serializers

# Default serializer
# @bind: [POST] new user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

# User minimal only serializer
class UserMinimumSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "did",
            "display_name",
        )

# Human readable serializer for employer
class EmployerReadableSerializer(UserMinimumSerializer):
    class Meta:
        model = get_user_model()
        fields = UserMinimumSerializer.Meta.fields + (
            "contact",
            "email",
            "address",
        )

# Human readable serializer for employee
class EmployeeReadableSerializer(EmployerReadableSerializer):
    class Meta:
        model = get_user_model()
        fields = EmployerReadableSerializer.Meta.fields + (
            "birth",
        )
