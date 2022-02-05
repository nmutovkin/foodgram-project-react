from re import search

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Name', max_length=30)
    color = models.CharField('Color', max_length=30)
    slug = models.SlugField('Slug', unique=True)

    def clean(self):
        if not search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', self.color):
            raise ValidationError("Color is not a hex code")

    def __str__(self):
        return self.name


class IngredientType(models.Model):
    name = models.CharField('Name', max_length=100)
    measurement_unit = models.CharField('Measurement unit', max_length=30)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    ingredient_type = models.ForeignKey(
        IngredientType,
        on_delete=models.CASCADE,
        verbose_name='Ingredient',
        related_name='ingredients'
    )
    amount = models.PositiveSmallIntegerField('Amount')

    def __str__(self):
        return (f'{self.ingredient_type.name}, '
                f'{self.amount} {self.ingredient_type.measurement_unit}')


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Author'
    )
    name = models.CharField('Name', max_length=200)
    image = models.ImageField(
        'Image',
        upload_to='recipes/',
        blank=True,
    )
    text = models.TextField('Description')
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ingredients'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Tags',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField('Cooking time')
    pub_date = models.DateTimeField(
        'Publication date',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='User'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Recipe'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite')
        ]

    def __str__(self):
        return f"{self.recipe} is favorited by {self.user}"


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='User'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Recipe'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_cart')
        ]

    def __str__(self):
        return f"{self.recipe} is in shopping cart of {self.user}"
