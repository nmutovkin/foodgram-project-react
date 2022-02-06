from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientType, Recipe,
                            ShoppingCart, Tag)
from rest_framework import serializers
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = fields


class IngredientTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientType
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = fields


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient_type.id')
    name = serializers.CharField(source='ingredient_type.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient_type.measurement_unit', read_only=True
    )

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(("Убедитесь, что это значение "
                                               "больше 1."))
        return value


class RecipeReadSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    image = serializers.SerializerMethodField(read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    def get_is_favorited(self, obj):
        current_user = self.context['request'].user

        if current_user.is_anonymous:
            return False

        fav_object = Favorite.objects.filter(
            user=current_user,
            recipe=obj
        )

        return fav_object.exists()

    def get_is_in_shopping_cart(self, obj):
        current_user = self.context['request'].user

        if current_user.is_anonymous:
            return False

        cart_object = ShoppingCart.objects.filter(
            user=current_user,
            recipe=obj
        )

        return cart_object.exists()

    def get_image(self, obj):
        return obj.image.url

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'image',
            'name', 'text', 'cooking_time', 'is_favorited',
            'is_in_shopping_cart'
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'tags', 'ingredients', 'image',
            'name', 'text', 'cooking_time'
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        ingredient_objects = []
        for ingredient in ingredients:
            type_id = list(ingredient.items())[0][1]['id']
            amount = list(ingredient.items())[1][1]

            ingredient_type_object, _ = IngredientType.objects.get_or_create(
                id=type_id
            )
            ingredient_object, _ = Ingredient.objects.get_or_create(
                ingredient_type=ingredient_type_object, amount=amount
            )
            ingredient_objects.append(ingredient_object)

        recipe.tags.add(*tags)
        recipe.ingredients.add(*ingredient_objects)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])

        instance = super().update(instance, validated_data)
        if tags:
            instance.tags.clear()
        if ingredients:
            instance.ingredients.clear()

        for tag in tags:
            tag_object, _ = Tag.objects.get_or_create(
                pk=tag.id
            )
            instance.tags.add(tag_object)

        for ingredient in ingredients:
            type_id = list(ingredient.items())[0][1]['id']
            amount = list(ingredient.items())[1][1]

            ingredient_type_object, _ = IngredientType.objects.get_or_create(
                id=type_id
            )

            ingredient_object, _ = Ingredient.objects.get_or_create(
                ingredient_type=ingredient_type_object, amount=amount
            )

            instance.ingredients.add(ingredient_object)

        return instance

    def to_representation(self, instance):
        s = RecipeReadSerializer(context=self.context)
        return s.to_representation(instance=instance)

    def validate_cooking_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(("Время приготовления должно"
                                               "быть больше 0"))
        return value


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id', 'image',
            'name', 'cooking_time'
        )
        read_only_fields = fields
