from django.shortcuts import render
from django.http import HttpRequest

def authorization(request: HttpRequest):
    return render(request, 'main/authorization.html')

def button_laboratory(request: HttpRequest):
    return render(request, 'main/butlab.html')