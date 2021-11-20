from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    patronymic = models.CharField('Отчество', 
                                  max_length=150, 
                                  blank=True,
                                  default=''
                                  )
    phone = PhoneNumberField('Мобильный телефон', 
                             null=True,
                             help_text='Введите номер телефона, например, +79999999999')
    passport = models.CharField('Номер паспорта', 
                                max_length=30, 
                                default=''
                                )
    birthday_date = models.DateField('Дата рождения',
                                     null=True,
                                     db_index=True)
    consent_to_processing_db = models.BooleanField(
        'согласие на обработку персональных данных', default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


