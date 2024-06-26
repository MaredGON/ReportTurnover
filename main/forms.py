from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import CustomUser, Subject, LecturerSubject, Laboratory, Laboratory_Status


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'name', 'surname', 'patronymic', 'role', 'password1', 'password2')


class SubjectCreationForm(ModelForm):

    class Meta:
        model = Subject
        fields = ('title',)

    def save(self, commit=False):
        subject = super().save(commit=False)
        if commit:
            subject.save()
        return subject

class LaboratoryCreationForm(ModelForm):

    class Meta:
        model = Laboratory
        fields = ('title', 'educational', 'lecturer')

    def save(self, commit=False):
        lab = super().save(commit=False)
        if commit:
            lab.save()
        return lab