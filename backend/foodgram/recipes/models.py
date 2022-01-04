from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название', max_length=30)
    color = models.CharField('Цвет', max_length=30)
    slug = models.SlugField('Имя тэга', unique=True)


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=100)
    quantity = models.PositiveSmallIntegerField('Количество')
    measurement_unit = models.CharField('Единица измерения', max_length=30)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField('Название', max_length=30)
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True,
    )
    description = models.TextField('Описание')
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
    time = models.PositiveSmallIntegerField('Время приготовления')


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='follower',
        verbose_name='Подписчик',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='following',
        verbose_name='Автор',
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow')
        ]

    def __str__(self):
        return str(self.user) + " follows " + str(self.author)
