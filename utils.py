from main.models import Student, Laboratory_Status, Laboratory, CustomUser, Lecturer
from django.db.models.signals import post_save
from django.dispatch import receiver



def create_laboratory_status_for_students(laboratory_instance):
    students = Student.objects.all()
    for student in students:
        Laboratory_Status.objects.get_or_create(laboratory=laboratory_instance, student=student)

def create_laboratory_status_one_student(student_instance):
    laboratorys = Laboratory.objects.all()
    for laboratory in laboratorys:
        Laboratory_Status.objects.get_or_create(laboratory=laboratory, student=student_instance)


@receiver(post_save, sender=CustomUser)
def create_lecturer(sender, instance, created, **kwargs):
    if created:
        if instance.role == CustomUser.ROLE_LECTURER:
            Lecturer.objects.create(user=instance)
        elif instance.role == CustomUser.ROLE_STUDENT:
            Student.objects.create(user=instance)

