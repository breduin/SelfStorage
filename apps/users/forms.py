from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.html import format_html

from .models import User


class CreateUserForm(UserCreationForm):
    birthday_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'},
                                                        format='%Y-%m-%d'),
                                 label='Дата рождения',
                                 error_messages={'required': ''})
    consent_to_processing_db = forms.BooleanField(
        label=format_html(
            'Согласие на обработку <a href="{}">персональных данных</a>',
            'https://raw.githubusercontent.com/Fiskless/where-to-go/main/static/pd_aggreement.jpg'
        )
    )

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
