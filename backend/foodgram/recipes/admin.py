from django.contrib import admin
from .models import IngredientType, Tag

admin.site.register(Tag)
admin.site.register(IngredientType)
