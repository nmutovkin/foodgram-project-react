from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import models
from re import search

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название', max_length=30)
    color = models.CharField('Цвет', max_length=30)
    slug = models.SlugField('Имя тэга', unique=True)

    def clean(self):
        if not search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', self.color):
            raise ValidationError("Color is not a hex code")

    def __str__(self):
        return self.name


class IngredientType(models.Model):
    name = models.CharField('Название', max_length=100)
    measurement_unit = models.CharField('Единица измерения', max_length=30)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    ingredient_type = models.ForeignKey(
        IngredientType,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredients'
    )
    amount = models.PositiveSmallIntegerField('Количество')


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField('Название', max_length=200)
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True,
    )
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f"{self.recipe} is favorited by {self.user}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f"{self.recipe} is in shopping cart of {self.user}"
