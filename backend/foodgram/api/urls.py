from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientTypeViewSet, TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientTypeViewSet)

urlpatterns = [
    path('', include(router.urls))
]
