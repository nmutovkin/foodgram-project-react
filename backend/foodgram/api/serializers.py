from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'is_subscribed'
        )
        read_only_fields = ('id', )


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password'
        )
        read_only_fields = ('id', )

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "User with this email already exists"
            )
        return value


class SubscribeSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'is_subscribed'
        )
        read_only_fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'is_subscribed'
        )
