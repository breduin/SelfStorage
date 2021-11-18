from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils import timezone

from .models import User

class CreateUserForm(UserCreationForm):
    birthday_date = forms.DateField(label='Дата рождения', initial=(timezone.now))

    class Meta:
        model = User
        fields = ['username',
                  'password1',
                  'password2',
                  'phone',
                  'first_name',
                  'last_name',
                  'patronymic',
                  'passport',
                  'birthday_date',
                  'consent_to_processing_db'
                  ]


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
