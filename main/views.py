from operator import ne

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm, SubjectCreationForm, LaboratoryCreationForm
from .models import CustomUser, Lecturer, Student, LecturerSubject, Laboratory, Laboratory_Status
from utils import create_laboratory_status_for_students, create_laboratory_status_one_student

def authorization(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request, 'main/authorization.html')

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(username=username, password=password)
    if user is not None and user.role == CustomUser.ROLE_LECTURER:
        login(request, user)
        next_url = request.GET.get("next")
        if next_url:
            return redirect(next_url)
        else:
            return HttpResponse("Вы авторизовались")
    else:
        return render(request, 'main/authorization.html', {"error":"Incorrect login or password. Try again!"})

def user_logout(request:HttpRequest):
    logout(request)
    return redirect('authorization')

class CreateUserView(LoginRequiredMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user_success_create')
    template_name = 'main/create.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()

        if user.role == CustomUser.ROLE_STUDENT:
            student, status = Student.objects.get_or_create(user=user)
            create_laboratory_status_one_student(student)
        elif user.role == CustomUser.ROLE_LECTURER:
            Lecturer.objects.get_or_create(user=user)

        return response


class CreateSubjectView(LoginRequiredMixin, CreateView):
    form_class = SubjectCreationForm
    success_url = reverse_lazy('user_success_create')
    template_name = 'main/create_subject.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user

        if user.is_authenticated:
            subject = form.save(commit=True)
            LecturerSubject.objects.get_or_create(lecturer=Lecturer.objects.get(user=user),
                                                  subject=subject
                                                  )
            return response

        else:
            return render(template_name=self.template_name,
                          context={
                              "error":"You are not authorized"
                          },
                          request=self.request)


class CreateLaboratoryView(LoginRequiredMixin, CreateView):
    form_class = LaboratoryCreationForm
    success_url = reverse_lazy('user_success_create')
    template_name = 'main/create_laboratory.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user

        if user.is_authenticated:
            laboratory = form.save(commit=False)
            userlecturer = laboratory.lecturer
            subject = laboratory.educational
            if LecturerSubject.objects.filter(lecturer=userlecturer, subject=subject).exists():
                laboratory = form.save(commit=True)
                create_laboratory_status_for_students(laboratory)
                return response

            else:
                return render(template_name=self.template_name,
                              context={
                                  "error": "You have chosen a subject that does not meet the requirements of this teacher"
                              },
                              request=self.request)

        else:
            return render(template_name=self.template_name,
                          context={
                              "error":"You are not authorized"
                          },
                          request=self.request)


def success_create_user(request):
    users = CustomUser.objects.all()
    context = {
        "alert_message": "Пользователь успешно создан",
        "users": users,
    }
    return render(request, context=context, template_name="main/list.html")


@login_required
def button_laboratory(request: HttpRequest, pk):
    try:
        laboratory_status = Laboratory_Status.objects.get(id=pk)
        laboratory_status.additional_status = Laboratory_Status.ADDITIONAL_STATUS_VIEWED
        student = laboratory_status.student
        context = {
            'studentname' : student.user.name,
            'studentsurname': student.user.surname,
            'result' : False,
        }

        if request.method == 'GET':
            return render(request, 'main/lab_check.html', context=context)

        comment = request.POST["comment"]
        status = request.POST["status"]
        laboratory_status.lecturer_comment = comment
        if status=="yes":
            laboratory_status.status = Laboratory_Status.STATUS_ACCEPT
        else:
            laboratory_status.status = Laboratory_Status.STATUS_REJECT
        laboratory_status.save()
        context['result'] = True

        return render(request, 'main/lab_check.html', context=context)

    except Laboratory_Status.DoesNotExist:
        return HttpResponse('Такой лабораторной работы не существует!')

