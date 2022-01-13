from rest_framework import serializers
from recipes.models import Ingredient, IngredientType, Recipe, Tag
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


class RecipeReadSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'text', 'cooking_time'
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'tags', 'ingredients',
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

    def to_representation(self, instance):
        s = RecipeReadSerializer()
        return s.to_representation(instance=instance)
