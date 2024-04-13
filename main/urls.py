from django.urls import path
from . import views

urlpatterns = [
    path('butlab', views.button_laboratory, name= 'butlab'),
    path('authorization', views.authorization, name= 'authorization'),
]