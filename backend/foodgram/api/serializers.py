from rest_framework import serializers
from recipes.models import IngredientType, Tag


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
