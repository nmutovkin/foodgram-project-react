from django.db.models import base
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientTypeViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientTypeViewSet)
router.register('recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls))
]
