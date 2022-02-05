# Generated by Django 2.2.16 on 2022-02-05 11:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20220205_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='favorites',
                to='recipes.Recipe',
                verbose_name='Recipe'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='favorites',
                to=settings.AUTH_USER_MODEL,
                verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='amount',
            field=models.PositiveSmallIntegerField(verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='ingredient_type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ingredients',
                to='recipes.IngredientType',
                verbose_name='Ingredient'),
        ),
        migrations.AlterField(
            model_name='ingredienttype',
            name='measurement_unit',
            field=models.CharField(
                max_length=30,
                verbose_name='Measurement unit'),
        ),
        migrations.AlterField(
            model_name='ingredienttype',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='recipes',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(
                verbose_name='Cooking time'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(
                blank=True, upload_to='recipes/',
                verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(
                related_name='recipes',
                to='recipes.Ingredient',
                verbose_name='Ingredients'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(
                auto_now_add=True,
                verbose_name='Publication date'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(
                related_name='recipes',
                to='recipes.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='cart', to='recipes.Recipe',
                verbose_name='Recipe'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='cart', to=settings.AUTH_USER_MODEL,
                verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=30, verbose_name='Color'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug'),
        ),
    ]
