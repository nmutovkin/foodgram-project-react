# Generated by Django 2.2.16 on 2022-02-08 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_auto_20220205_1142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={
                'ordering': ['user__username'],
                'verbose_name': 'Favorite',
                'verbose_name_plural': 'Favorites'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={
                'ordering': ['ingredient_type__name'],
                'verbose_name': 'Ingredient',
                'verbose_name_plural': 'Ingredients'},
        ),
        migrations.AlterModelOptions(
            name='ingredienttype',
            options={
                'ordering': ['name'],
                'verbose_name': 'Ingredient type',
                'verbose_name_plural': 'Ingredient types'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={
                'ordering': ['-pub_date'],
                'verbose_name': 'Recipe',
                'verbose_name_plural': 'Recipes'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={
                'ordering': ['user__username'],
                'verbose_name': 'Shopping cart',
                'verbose_name_plural': 'Shopping carts'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={
                'ordering': ['name'],
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags'},
        ),
    ]
