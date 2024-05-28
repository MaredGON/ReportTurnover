from main.models import Student, Laboratory_Status, Laboratory, CustomUser, Lecturer, Subject

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.transaction import Atomic
from asgiref.sync import sync_to_async
from aiogram.dispatcher import FSMContext
import segno

from main.API_TG.configs.loader import bot
from djangoProject.settings import ALLOWED_HOSTS



def create_laboratory_status_for_students(laboratory_instance):
    students = Student.objects.all()
    for student in students:
        Laboratory_Status.objects.get_or_create(laboratory=laboratory_instance, student=student)


def create_laboratory_status_one_student(student_instance):
    laboratorys = Laboratory.objects.all()
    for laboratory in laboratorys:
        Laboratory_Status.objects.get_or_create(laboratory=laboratory, student=student_instance)



class AsyncAtomicContext(Atomic):
    def __init__(self, using=None, savepoint=True, durable=False):
        super().__init__(using, savepoint, durable)

    async def __aenter__(self):
        await sync_to_async(super().__enter__)()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await sync_to_async(super().__exit__)(exc_type, exc_value, traceback)

async def is_student_register(chat_id: int) -> bool:
    try:
        student = await sync_to_async(Student.objects.get)(chat=chat_id)
        return True
    except Exception as e:
        return False

async def generator_qr(pk):
    host = ALLOWED_HOSTS[0]
    result_string = f'http://{host}:8000/butlab/{pk}/'
    qrcode = segno.make_qr(result_string)
    path_photo = f"C:\QRIMAGES\qr{pk}.png"
    qrcode.save(path_photo, scale=10)
    return path_photo

async def get_laboratory_status(data):
    try:
        student = data.get('student')
        educational_title = data.get('educational')
        laboratory_title = data.get('title_lab')
        async with AsyncAtomicContext():
            educational = await sync_to_async(Subject.objects.get)(title=educational_title)
            laboratory = await sync_to_async(Laboratory.objects.get)(title=laboratory_title, educational=educational)
            laboratory_status = await sync_to_async(Laboratory_Status.objects.get)(student=student,
                                                                                   laboratory=laboratory)
            return laboratory_status
    except Exception as e:
        print(str(e))

async def send_notification(chat, comment, title, status, subject):
    textmessage = (f"Преподаватель посмотрел лабораторную работу {str(title).lower()} по предмету {str(subject).lower()}\n\n"
                   f"Комментарий - {comment}\n"
                   f"Статус сдачи - {status}\n")
    await bot.send_message(text=textmessage, chat_id=chat)


