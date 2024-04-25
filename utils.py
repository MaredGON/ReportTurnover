from main.models import Student, Laboratory_Status, Laboratory, CustomUser

def create_laboratory_status_for_students(laboratory_instance):
    students = Student.objects.all()
    for student in students:
        Laboratory_Status.objects.get_or_create(laboratory=laboratory_instance, student=student)

def create_laboratory_status_one_student(student_instance):
    laboratorys = Laboratory.objects.all()
    for laboratory in laboratorys:
        Laboratory_Status.objects.get_or_create(laboratory=laboratory, student=student_instance)



