from django.contrib import admin
from .models import IngredientType, Recipe, Tag

admin.site.register(Tag)
admin.site.register(IngredientType)
admin.site.register(Recipe)
