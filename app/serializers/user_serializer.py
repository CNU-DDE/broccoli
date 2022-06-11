from django.contrib.auth import get_user_model
from rest_framework import serializers

# Default serializer
# @bind: [POST] new user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

# Display name only serializer
class UserDisplayNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("display_name",)

# DID and display name for employer
class UserPublicKeySerializer(UserDisplayNameSerializer):
    class Meta:
        model = get_user_model()
        fields = UserDisplayNameSerializer.Meta.fields + (
            "did",
            "public_key",
            "wallet_address",
        )

# Human readable serializer for employer
class EmployerReadableSerializer(UserDisplayNameSerializer):
    class Meta:
        model = get_user_model()
        fields = UserDisplayNameSerializer.Meta.fields + (
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
