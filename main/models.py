from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    surname2 = models.CharField(max_length=100, null=True, blank=True)
    chat = models.IntegerField(null=True, blank=True)
    group = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Lecturer(models.Model):
    username = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    surname2 = models.CharField(max_length=100, null=True, blank=True)
    key = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


class Educational(models.Model):
    title = models.TextField()
    lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT)


class Laboratory(models.Model):
    class Meta:
        ordering = ['educational_id', 'created_at']

    title = models.CharField(max_length=100)
    educational = models.ForeignKey(Educational, on_delete=models.SET_NULL, null=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class Laboratory_Status(models.Model):
    lab = models.ForeignKey(Laboratory, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    viewed = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

