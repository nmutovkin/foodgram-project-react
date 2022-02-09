from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientType, Recipe,
                     ShoppingCart, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'get_favorites_count')
    list_filter = ('name', 'author', 'tags')

    def get_favorites_count(self, obj):
        fav_object = Favorite.objects.filter(
            recipe=obj
        )
        return fav_object.count()
    get_favorites_count.short_description = 'Number of users favorited'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class IngredientTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'amount', 'get_measurement_unit')
    search_fields = ('ingredient_type__name', )

    def get_name(self, obj):
        return obj.ingredient_type.name
    get_name.short_description = 'Ingredient name'

    def get_measurement_unit(self, obj):
        return obj.ingredient_type.measurement_unit
    get_measurement_unit.short_description = 'Measurement unit'


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientType, IngredientTypeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoritesAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
