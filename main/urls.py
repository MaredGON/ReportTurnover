from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path('butlab/<int:pk>/', views.button_laboratory, name='butlab'),
    path('authorization',
         views.authorization,
         name='authorization'
         ),
    path("create/", views.CreateUserView.as_view(), name="user_create", ),
    path("logout/", views.user_logout, name="user_logout"),
    path("createsubject/", views.CreateSubjectView.as_view(), name="subject_create"),
    path("createlab/", views.CreateLaboratoryView.as_view(), name="lab_create"),
    path("success_create/", views.success_create_user, name="user_success_create"),
]