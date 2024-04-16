from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path('butlab', views.button_laboratory, name='butlab'),
    path('authorization',
         views.authorization,
         name='authorization'
         ),
    path("create/", views.CreateUserView.as_view(), name="user_create", ),
    path("logout/", views.user_logout, name="user_logout"),
    path("success_create/", views.success_create_user, name="user_success_create"),
]