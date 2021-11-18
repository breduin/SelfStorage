from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.html import format_html

from .models import User

class CreateUserForm(UserCreationForm):
    birthday_date = forms.DateField(label='Дата рождения', initial=(timezone.now))
    consent_to_processing_db = forms.BooleanField(label=format_html('Согласие на обработку <a href="{}">персональных данных</a>', 'https://vc.ru/legal/133217-soglasie-na-obrabotku-personalnyh-dannyh-blank-2020-goda/'))

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
