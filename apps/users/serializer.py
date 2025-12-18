import re
from typing import Any

from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from apps.users.models import User

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role"
        ]

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "role",
            "birthday",
            "phone_number",
            "password",
            "re_password",
        ]

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        password = attrs.get('password')
        re_password = attrs.pop('re_password', None)

        re_pattern = r"^[a-zA-Z]+$"

        if not re.match(re_pattern, first_name):
            raise serializers.ValidationError(
                {
                    "first_name": "Must contain only Latin characters"
                }
            )

        if not re.match(re_pattern, last_name):
            raise serializers.ValidationError(
                {
                    "last_name": "Must contain only Latin characters"
                }
            )

        if not password:
            raise serializers.ValidationError(
                {
                    "password": "Field is required"
                }
            )

        if not re_password:
            raise serializers.ValidationError(
                {
                    "re_password": "Field is required"
                }
            )

        validate_password(password)

        if password != re_password:
            raise serializers.ValidationError(
                {
                    "re_password": "Passwords must match"
                }
            )

        return attrs

    def create(self, validated_data: dict[str, Any]) -> User:
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)

        user.save()

        return user

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'