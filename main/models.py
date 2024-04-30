from django.db import models
from django.contrib.auth.models import AbstractUser

class SimpleBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


class EducationalGroup(SimpleBaseModel):
    number = models.CharField(max_length=100, null=True, blank=True, verbose_name="Номер группы")
    description = models.CharField(
        max_length=500, null=True, blank=True, default=None, verbose_name="Описание")

    class Meta:
        verbose_name = "Группы"
        verbose_name_plural = "Группы"

    def __str__(self):
        return f'{self.number}'


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
        from .models import Student, Lecturer

        if self.role == self.ROLE_STUDENT:
            return Student.objects.filter(user=self).first()
        elif self.role == self.ROLE_LECTURER:
            return Lecturer.objects.filter(user=self).first()
        return


class Student(SimpleBaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    group = models.ForeignKey(EducationalGroup, null=True, blank=True, on_delete=models.SET_NULL)
    chat = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Студенты"
        verbose_name_plural = "Студенты"
    def __str__(self):
        return f'{self.user.name} {self.user.surname}'


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
    title = models.CharField(max_length=100, verbose_name='Название')
    educational = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, verbose_name='Предмет')
    lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT, verbose_name='Преподаватель')

    class Meta:
        verbose_name = 'Лабораторные работы'
        verbose_name_plural = 'Лабораторные работы'

    def __str__(self):
        return f'{self.title}'



class Laboratory_Status(SimpleBaseModel):
    STATUS_ACCEPT = "Сдано"
    STATUS_REJECT = "Не сдано"
    ADDITIONAL_STATUS_VIEWED = "Просмотрено"
    ADDITIONAL_STATUS_NOT_VIEWED = "Не просмотрено"
    STUDENT_STATUS_GENERATED = "Сгенерировал QR"
    STUDENT_STATUS_NOT_GENERATED = "Не сгенерировал QR"

    STATUS_ACCEPTANCES_CHOICES = (
        (STATUS_ACCEPT, STATUS_ACCEPT),
        (STATUS_REJECT, STATUS_REJECT),
    )

    STATUS_VIEWEDS_CHOICES = (
        (ADDITIONAL_STATUS_VIEWED, ADDITIONAL_STATUS_VIEWED),
        (ADDITIONAL_STATUS_NOT_VIEWED, ADDITIONAL_STATUS_NOT_VIEWED),
    )

    STATUS_GENERATED_CHOICES = (
        (STUDENT_STATUS_GENERATED, STUDENT_STATUS_GENERATED),
        (STUDENT_STATUS_NOT_GENERATED, STUDENT_STATUS_NOT_GENERATED),
    )

    student = models.ForeignKey(Student, on_delete=models.PROTECT, verbose_name="Студент")
    laboratory = models.ForeignKey(
        Laboratory, on_delete=models.PROTECT, verbose_name="Лабораторная работа" )
    status = models.CharField(
        max_length=50, null=True, blank=True, choices=STATUS_ACCEPTANCES_CHOICES, default=STATUS_REJECT, verbose_name="Статус сдачи")
    additional_status = models.CharField(
        max_length=50, null=True, blank=True, choices=STATUS_VIEWEDS_CHOICES,
        default=ADDITIONAL_STATUS_NOT_VIEWED, verbose_name="Статус просмотра"
    )
    student_status =models.CharField(
        max_length=50, null=True, blank=True, choices=STATUS_GENERATED_CHOICES,
        default=STUDENT_STATUS_NOT_GENERATED, verbose_name="Статус студента"
    )
    lecturer_comment = models.CharField(
        max_length=500, null=True, blank=True, default=None, verbose_name="Комментарий преподавателя")
    student_comment = models.CharField(
        max_length=500, null=True, blank=True, default=None, verbose_name="Комментарий студента")

    class Meta:
        verbose_name = "Статусы лабораторных работ по студентам"
        verbose_name_plural = "Статусы лабораторных работ по студентам"

    def __str__(self):
        return f'{self.laboratory}'


