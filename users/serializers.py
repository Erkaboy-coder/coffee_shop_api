from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "is_verified"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="User email address")
    password = serializers.CharField(write_only=True, help_text="User password")

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="User email used during signup.")
    code = serializers.CharField(max_length=6, help_text="6-digit verification code sent to console.")

class ResendCodeSerializer(serializers.Serializer):
    """Serializer for resending verification code."""
    email = serializers.EmailField(help_text="User email to resend verification code.")