from django.db.models import Exists, OuterRef
from django.http import HttpResponse
from rest_framework import mixins, pagination, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from recipes.models import Favorite, IngredientType, Recipe, ShoppingCart, Tag
from .serializers import (IngredientTypeSerializer, RecipeReadSerializer,
                          RecipeShortSerializer,
                          RecipeWriteSerializer, TagSerializer)
from users.pagination import CustomPageNumberPagination


class ListRetrieveViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class IngredientTypeViewSet(ListRetrieveViewSet):
    queryset = IngredientType.objects.all()
    serializer_class = IngredientTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Recipe.objects.all()
        favorites = Favorite.objects.filter(
            user=self.request.user,
            recipe=OuterRef('id')
        )
        cart = ShoppingCart.objects.filter(
            user=self.request.user,
            recipe=OuterRef('id')
        )
        queryset = queryset.annotate(is_favorited=Exists(favorites))
        return queryset.annotate(is_in_shopping_cart=Exists(cart))

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(RecipeViewSet, self).perform_update(serializer)

    def perform_destroy(self, serializer):
        if serializer.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        super(RecipeViewSet, self).perform_destroy(serializer)

    def add_to_special_list(self, request, Model, pk=None):
        recipe = self.get_object()
        user = request.user

        object = Model.objects.filter(
            user=user,
            recipe=recipe
        )

        if request.method == 'POST':
            serializer = RecipeShortSerializer(
                recipe,
                data=request.data
            )
            serializer.is_valid(raise_exception=True)

            if object.exists():
                return Response(
                    {'errors': 'object already added'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            Model.objects.get_or_create(user=user, recipe=recipe)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        else:  # DELETE

            if not object.exists():
                return Response(
                    {'errors': 'object is not in the list'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            object.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        return self.add_to_special_list(request, Favorite, pk)

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        return self.add_to_special_list(request, ShoppingCart, pk)

    @action(detail=False)
    def download_shopping_cart(self, request):

        queryset = self.get_queryset()
        cart_objects = ShoppingCart.objects.filter(user=request.user)
        recipes = queryset.filter(cart__in=cart_objects)

        ingredient_dict = dict()

        for recipe in recipes:
            for ingredient in recipe.ingredients.all():
                ingredient_type = ingredient.ingredient_type
                amount = ingredient.amount

                if ingredient_type in ingredient_dict:
                    ingredient_dict[ingredient_type] += amount
                else:
                    ingredient_dict[ingredient_type] = amount

        filename = 'shopping_ingredients.txt'
        lines = []

        for ing_type, amount in ingredient_dict.items():
            lines.append(f'{ing_type.name}, {amount}'
                         f' {ing_type.measurement_unit}')

        response_content = '\n'.join(lines)

        response = HttpResponse(response_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response
