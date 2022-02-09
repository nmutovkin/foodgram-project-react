from django.db.models import Sum
from django.http import HttpResponse
from django_filters import AllValuesMultipleFilter, FilterSet, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientType, Recipe,
                            ShoppingCart, Tag)
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from users.pagination import CustomPageNumberPagination

from .serializers import (IngredientTypeSerializer, RecipeReadSerializer,
                          RecipeShortSerializer, RecipeWriteSerializer,
                          TagSerializer)


class ListRetrieveViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    pass


class TagViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = None


class CustomSearchFilter(filters.SearchFilter):
    search_param = 'name'


class IngredientTypeViewSet(ListRetrieveViewSet):
    queryset = IngredientType.objects.all()
    serializer_class = IngredientTypeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = [CustomSearchFilter]
    pagination_class = None
    search_fields = ['^name']


class RecipeFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = NumberFilter(method='get_is_favorited')
    is_in_shopping_cart = NumberFilter(method='get_is_in_shopping_cart')
    author = NumberFilter(field_name='author__id')

    def get_is_favorited(self, queryset, name, value):
        if value == 1:
            return queryset.filter(favorites__user=self.request.user)
        else:
            return queryset.exclude(favorites__user=self.request.user)

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value == 1:
            return queryset.filter(cart__user=self.request.user)
        else:
            return queryset.exclude(cart__user=self.request.user)

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
            'author'
        )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

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

    def add_to_special_list(self, request, model, pk=None):
        recipe = self.get_object()
        user = request.user

        object = model.objects.filter(
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

            model.objects.get_or_create(user=user, recipe=recipe)
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

        ingredients = Ingredient.objects.filter(recipes__in=recipes)
        ing_types = IngredientType.objects.filter(
            ingredients__in=ingredients
        ).annotate(amount=Sum('ingredients__amount'))

        lines = [f'{ing_type.name}, {ing_type.amount}'
                 f' {ing_type.measurement_unit}' for ing_type in ing_types]

        filename = 'shopping_ingredients.txt'

        response_content = '\n'.join(lines)

        response = HttpResponse(response_content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
