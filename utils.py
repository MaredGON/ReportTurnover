from main.models import Student, Laboratory_Status

def create_laboratory_status_for_students(laboratory_instance):
    students = Student.objects.all()
    for student in students:
        Laboratory_Status.objects.create(lab=laboratory_instance, student=student)