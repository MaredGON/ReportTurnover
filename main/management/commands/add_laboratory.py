from django.core.management import BaseCommand

from main.models import Laboratory, Educational, Lecturer, Student, Laboratory_Status
from utils import create_laboratory_status_for_students

class Command(BaseCommand):
    help = 'Создается новый объект Laboratory в базе данных'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str, help='Название лабораторной работы')
        parser.add_argument('educational', type=str, help='Предмет лабораторной работы')
        parser.add_argument('lecturer', type=str, help='Логин преподавателя-создателя лабораторной работы')


    def handle(self, *args, **options):
        title_value = options['title']
        educational_value = options['educational']
        lecturer_username_value = options['lecturer']

        try:
            lecturer = Lecturer.objects.get(username=lecturer_username_value)
        except Lecturer.DoesNotExist:
            self.stdout.write(self.style.ERROR('Преподаватель с таким логином не существует'))
            return

        try:
            educational = Educational.objects.get(title=educational_value)
        except Educational.DoesNotExist:
            self.stdout.write(self.style.ERROR('Предмет с таким названием не существует'))
            self.stdout.write(self.style.ERROR(educational_value))
            return

        existing_title = Laboratory.objects.filter(title=title_value).exists()
        if existing_title:
            self.stdout.write(self.style.ERROR('Лабораторная работа с таким названием уже существует'))
            return

        laboratory_object, create_state = Laboratory.objects.get_or_create(
                                                                title=title_value,
                                                                educational=educational,
                                                                lecturer=lecturer
                                                            )
        create_laboratory_status_for_students(laboratory_object)
        if create_state:
            self.stdout.write(self.style.SUCCESS(f'Создана новая лабораторная: {laboratory_object.title}'))
        else:
            self.stdout.write(self.style.WARNING('Произошла ошибка'))


