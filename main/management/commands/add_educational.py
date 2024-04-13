from django.core.management import BaseCommand

from main.models import Educational, Lecturer

class Command(BaseCommand):
    help = 'Создается новый объект Educational в базе данных'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str, help='Название предмета')
        parser.add_argument('lecturer', type=str, help='Логин преподавателя')

    def handle(self, *args, **options):
        title_value = options['title']
        lecturer_username_value = options['lecturer']

        try:
            lecturer = Lecturer.objects.get(username=lecturer_username_value)
        except Lecturer.DoesNotExist:
            self.stdout.write(self.style.ERROR('Преподаватель с таким логином не существует'))
            return

        existing_educational = Educational.objects.filter(title=title_value).exists()
        if existing_educational:
            self.stdout.write(self.style.ERROR('Предмет с таким названием уже существует'))
            return

        educational_object, create_state = Educational.objects.get_or_create(
            title=title_value,
            lecturer=lecturer
        )

        if create_state:
            self.stdout.write(self.style.SUCCESS(f'Создан новый предмет: {educational_object.title}'))
        else:
            self.stdout.write(self.style.WARNING('Произошла ошибка'))