from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm
from .models import CustomUser, Lecturer, Student

def authorization(request: HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('butlab')
        return render(request, 'main/authorization.html')

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(username=username, password=password)
    if user is not None and user.role == CustomUser.ROLE_LECTURER:
        login(request, user)
        return redirect('butlab')
    return render(request, 'main/authorization.html', {"error":"Incorrect login or password. Try again!"})

def user_logout(request:HttpRequest):
    logout(request)
    return redirect('authorization')

class CreateUserView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('user_success_create')
    template_name = 'main/create.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()

        if user.role == CustomUser.ROLE_STUDENT:
            Student.objects.create(user=user)
        elif user.role == CustomUser.ROLE_LECTURER:
            Lecturer.objects.create(user=user)

        return response

def success_create_user(request):
    users = CustomUser.objects.all()
    context = {
        "alert_message": "Пользователь успешно создан",
        "user": users,
    }
    return render(request, context=context, template_name="main/list.html")

def button_laboratory(request: HttpRequest):
    return render(request, 'main/lab_check.html')