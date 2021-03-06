from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from users.models import Follow

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'is_subscribed'
        )
        read_only_fields = ('id', )

    def get_is_subscribed(self, obj):
        current_user = self.context['request'].user

        if current_user.is_anonymous:
            return False

        follow_object = Follow.objects.filter(
            user=current_user,
            author=obj
        )

        return follow_object.exists()


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


class SubscribeSerializer(CustomUserSerializer):

    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    def get_recipes(self, obj):
        from api.serializers import RecipeShortSerializer
        request = self.context['request']
        recipes_limit = request.query_params.get('recipes_limit') or 10
        recipes_limit = int(recipes_limit)
        recipes = obj.recipes.all()[:recipes_limit]
        return RecipeShortSerializer(recipes, read_only=True, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'is_subscribed',
            'recipes', 'recipes_count'
        )
        read_only_fields = fields
