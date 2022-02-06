import csv

from django.core.management import BaseCommand
from recipes.models import IngredientType


class Command(BaseCommand):
    help = 'Load an ingredient csv file into the database'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt') as f:
            reader = csv.reader(f, dialect='excel', delimiter=',')
            for row in reader:
                IngredientType.objects.create(
                    name=row[0],
                    measurement_unit=row[1]
                )
