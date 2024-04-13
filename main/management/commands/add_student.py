from django.core.management import BaseCommand

from main.models import Student

class Command(BaseCommand):
    help = 'Создается новый объект Student в базе данных'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Имя студента')
        parser.add_argument('surname', type=str, help='Фамилия студента')
        parser.add_argument('surname2', type=str, help='Отчество студента')
        parser.add_argument('chat', type=int, help='Чат id студента')
        parser.add_argument('group', type=str, help='Группа студента')

    def handle(self, *args, **options):
        name_value = options['name']
        surname_value = options['surname']
        surname2_value = options['surname2']
        chat_value = options['chat']
        group_value = options['group']
        student_object, create_state = Student.objects.get_or_create(name=name_value,
                                                                     surname=surname_value,
                                                                     surname2=surname2_value,
                                                                     chat=chat_value,
                                                                     group=group_value)

        if create_state:
            self.stdout.write(self.style.SUCCESS(f'Создан новый студент: {student_object.name} {student_object.surname}'))
        else:
            self.stdout.write(self.style.WARNING('Произошла ошибка'))