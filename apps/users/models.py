from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    passport = models.PositiveSmallIntegerField(null=True, verbose_name='Серия и номер паспорта')
    phone = models.PositiveSmallIntegerField(null=True, verbose_name='Номер телефона')

    # class Meta:
    #     db_table = 'customer'
