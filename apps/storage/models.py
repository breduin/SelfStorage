from django.db import models

from .validators import lat_validators, lng_validators
# Create your models here.


class Warehouse(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название склада')
    description = models.TextField(verbose_name='Подробное описание склада')
    address = models.CharField(unique=True, verbose_name='Адрес склада')
    phone = models.PositiveSmallIntegerField(verbose_name='Телефонный номер склада')
    latitude = models.FloatField(validators=lat_validators, verbose_name='Широта', )
    longitude = models.FloatField(validators=lng_validators, verbose_name='Долгота')
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'
        db_table = 'warehouses'


class UnitMeasurement(models.Model):
    name = models.CharField(max_length=100, verbose_name='Единица измерения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Единица измерения'
        verbose_name_plural = 'Единицы измерения'
        db_table = 'unit_measurements'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория')
    measurement = models.ForeignKey(UnitMeasurement, related_name='mes_name', verbose_name='Единица измерения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name= 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categories'