import asyncio

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy


from .forms import CustomUserCreationForm, SubjectCreationForm, LaboratoryCreationForm
from .models import CustomUser, Lecturer, Student, LecturerSubject, Laboratory_Status
from utils import (
    create_laboratory_status_for_students,
    create_laboratory_status_one_student,
    send_notification,
)


def authorization(request: HttpRequest):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("/admin/")
        return render(request, "main/authorization.html")

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(username=username, password=password)
    if user is not None and user.role == CustomUser.ROLE_LECTURER:
        login(request, user)
        next_url = request.GET.get("next")
        if next_url:
            return redirect(next_url)
        else:
            return render(
                request,
                "main/authorization.html",
                context={
                    "result" : "Вы успешно авторизовались"
                }
            )
    else:
        return render(
            request,
            "main/authorization.html",
            {"error": "Не верные данные. Попробуйте снова!"},
        )


def user_logout(request: HttpRequest):
    logout(request)
    return redirect("authorization")


class CreateUserView(LoginRequiredMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("user_success_create")
    template_name = "main/create.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        if user.role == CustomUser.ROLE_STUDENT:
            student, status = Student.objects.get_or_create(user=user)
            create_laboratory_status_one_student(student)
        elif user.role == CustomUser.ROLE_LECTURER:
            Lecturer.objects.get_or_create(user=user)
            user.is_staff = 1
            group = Group.objects.get(name='base_lecturer')
            group.user_set.add(user)
            user = form.save()
        return response


class CreateSubjectView(LoginRequiredMixin, CreateView):
    form_class = SubjectCreationForm
    success_url = reverse_lazy("user_success_create")
    template_name = "main/create_subject.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user

        if user.is_authenticated:
            subject = form.save(commit=False)
            lecturer = Lecturer.objects.get(user=user)

            LecturerSubject.objects.get_or_create(lecturer=lecturer, subject=subject)

            return response
        else:
            return render(
                template_name=self.template_name,
                context={"error": "Вы не авторизовались"},
                request=self.request,
            )


class CreateLaboratoryView(LoginRequiredMixin, CreateView):
    form_class = LaboratoryCreationForm
    success_url = reverse_lazy("user_success_create")
    template_name = "main/create_laboratory.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        context = {}

        if user.is_authenticated:
            laboratory = form.save(commit=False)
            userlecturer = laboratory.lecturer
            subject = laboratory.educational

            if LecturerSubject.objects.filter(
                lecturer=userlecturer, subject=subject
            ).exists():
                laboratory = form.save(commit=True)
                create_laboratory_status_for_students(laboratory)
                return response
            else:
                context = {
                    "error": "You have chosen a subject that does not meet the requirements of this teacher"
                }
        else:
            context = {"error": "You are not authorized"}

        return render(
            template_name=self.template_name, context=context, request=self.request
        )


def success_create_user(request):
    users = CustomUser.objects.all()
    context = {
        "alert_message": "Пользователь успешно создан",
        "users": users,
    }
    return render(request, context=context, template_name="main/list.html")


@login_required
def button_laboratory(request: HttpRequest, pk):
    laboratory_status = Laboratory_Status.objects.filter(id=pk).first()
    if not laboratory_status:
        return HttpRequest("Такой лабораторной работы не существует!")

    student = laboratory_status.student
    laboratory_status.additional_status = Laboratory_Status.ADDITIONAL_STATUS_VIEWED
    comment = laboratory_status.student_comment
    comment = comment.split("\n\n")[-2].split("->")[1]
    if len(comment) > 20:
        comment = comment[:19] + "..."
    context = {
        "studentname": student.user.name,
        "studentsurname": student.user.surname,
        "result": False,
        "pk": pk,
        "comment": comment,
    }

    if request.method == "GET":
        return render(request, "main/lab_check.html", context=context)
    context["result"] = True

    comment = request.POST.get("comment")
    status = request.POST.get("status")

    laboratory_status.lecturer_comment = comment
    laboratory_status.status = (
        Laboratory_Status.STATUS_ACCEPT
        if status == "yes"
        else Laboratory_Status.STATUS_REJECT
    )
    laboratory_status.save()

    chat = student.chat
    title_name = laboratory_status.laboratory.title
    lab_status = laboratory_status.status
    educational = laboratory_status.laboratory.educational
    asyncio.run(send_notification(chat, comment, title_name, lab_status, educational))

    return render(request, "main/lab_check.html", context=context)