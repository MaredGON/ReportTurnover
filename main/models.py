from django.db import models
from django.contrib.auth.models import AbstractUser

class SimpleBaseModel(models.Model):
    creasted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


class EducationalGroup(SimpleBaseModel):
    title = models.CharField(max_length=25)


class CustomUser(AbstractUser):
    ROLE_STUDENT = "Студент"
    ROLE_LECTURER = "Преподаватель"
    ROLE_TYPE = (
        (ROLE_STUDENT, ROLE_STUDENT),
        (ROLE_LECTURER, ROLE_LECTURER),
    )

    name = models.CharField(max_length=100, verbose_name="Имя", )
    surname = models.CharField(max_length=100, verbose_name="Фамилия", )
    patronymic = models.CharField(max_length=100, null=True, blank=True, verbose_name="Отчество", )
    role = models.CharField(max_length=25, choices=ROLE_TYPE,  null=True, )

    def __str__(self):
        return self.username

    def role_model(self):
        from educational.models import Student, Lecturer

        if self.role == self.ROLE_STUDENT:
            return Student.objects.filter(user=self).first()
        elif self.role == self.ROLE_LECTURER:
            return Lecturer.objects.filter(user=self).first()
        return


class Student(SimpleBaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(EducationalGroup, null=True, blank=True, on_delete=models.SET_NULL)
    chat = models.IntegerField(null=True, blank=True)


class Lecturer(SimpleBaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} {self.user.surname}"


class Subject(SimpleBaseModel):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title}"


class LecturerSubject(SimpleBaseModel):
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

class Laboratory(SimpleBaseModel):
    title = models.CharField(max_length=100)
    educational = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT)



class Laboratory_Status(SimpleBaseModel):
    STATUS_ACCEPT = "Сдано"
    STATUS_REJECT = "Не сдано"
    ADDITIONAL_STATUS_VIEWED = "Просмотрено"
    ADDITIONAL_STATUS_NOT_VIEWED = "Не просмотрено"
    STUDENT_STATUS_GENERATED = "Сгенерировал QR"
    STUDENT_STATUS_NOT_GENERATED = "Не сгенерировал QR"

    student = models.ForeignKey(Student, on_delete=models.PROTECT, )
    laboratory = models.ForeignKey(Laboratory, on_delete=models.PROTECT, )
    status = models.CharField(max_length=50, null=True, blank=True, default=STATUS_REJECT, )
    additional_status = models.CharField(
        max_length=50, null=True, blank=True, default=ADDITIONAL_STATUS_NOT_VIEWED,
    )
    student_status =models.CharField(
        max_length=50, null=True, blank=True, default=STUDENT_STATUS_NOT_GENERATED,
    )
    lecturer_comment = models.CharField(max_length=500, null=True, blank=True, default=None,)
    student_comment = models.CharField(max_length=500, null=True, blank=True, default=None, )
