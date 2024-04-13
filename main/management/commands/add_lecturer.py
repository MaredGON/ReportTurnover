from django.core.management import BaseCommand

from main.models import Lecturer

class Command(BaseCommand):
    help = 'Создается новый объект Student в базе данных'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Логин преподавателя')
        parser.add_argument('name', type=str, help='Имя преподавателя')
        parser.add_argument('surname', type=str, help='Фамилия преподавателя')
        parser.add_argument('surname2', type=str, help='Отчество преподавателя')
        parser.add_argument('key', type=str, help='Чат id студента')

    def handle(self, *args, **options):
        username_value = options['username']
        name_value = options['name']
        surname_value = options['surname']
        surname2_value = options['surname2']
        key_value = options['key']
        lecturer_object, create_state = Lecturer.objects.get_or_create(username=username_value,
                                                                       name=name_value,
                                                                       surname=surname_value,
                                                                       surname2=surname2_value,
                                                                       key=key_value)

        if create_state:
            self.stdout.write(self.style.SUCCESS(f'Создан новый преподаватель: {lecturer_object.name} {lecturer_object.surname}'))
        else:
            self.stdout.write(self.style.WARNING('Произошла ошибка'))