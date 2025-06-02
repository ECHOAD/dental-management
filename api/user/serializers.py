from __future__ import annotations

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from api.user.models import User


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "groups")
        extra_kwargs = {"password": {"write_only": True}}  # noqa: RUF012




    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(**validated_data)
        return user


class MinimalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")
        read_only_fields = ("id", "username", "email")

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User) -> Token:
        token = super().get_token(user)
        # Add custom claims
        groups = list(user.groups.values_list("name", flat=True))
        token["groups"] = groups
        token["name"] = (user.first_name  + user.last_name) or user.username
        return token
