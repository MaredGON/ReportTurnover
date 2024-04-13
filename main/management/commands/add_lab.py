from django.core.management import BaseCommand

from main.models import Laboratory


class Command(BaseCommand):
    help = 'Создается новый объект Lab в базе данных'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str, help='Название лабораторной')
        parser.add_argument('group', type=str, help='Группы')

    def handle(self, *args, **options):
        name_value = options['name']
        lab_object, create = Laboratory.objects.get_or_create(name=name_value)
        self.stdout.write(self.style.SUCCESS(f'Создана новая лабораторная работа: {lab_object}'))