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
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categories'


class PricePeriod(models.Model):
    period = models.CharField(max_length=100, verbose_name='Едииница времени')

    def __str__(self):
        return self.period

    class Meta:
        verbose_name = 'Базовое время аренды'
        verbose_name_plural = 'Базовое время аренды'
        db_table = 'price_periods'


class BaseStepPrice(models.Model):
    category = models.ForeignKey(Category, related_name='price', verbose_name='Категория')
    warehouse = models.ForeignKey(Warehouse, related_name='warehouse', verbose_name='Склад')
    base_price = models.FloatField(verbose_name='Базовая цена')
    step_price = models.FloatField(verbose_name='Шаг цены')

    def __str__(self):
        return self.base_price

    class Meta:
        verbose_name = 'Базовая цена'
        verbose_name_plural = 'Базовые цены'
        db_table = 'base_prices'


class Unit(models.Model):
    name = models.CharField(max_length=200, verbose_name='Объект аренды')
    category = models.ForeignKey(Category, related_name='category', verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объект аренды'
        verbose_name_plural = 'Объекты аренды'
        db_table = 'units'


class Price(models.Model):
    unit = models.ForeignKey(Unit, related_name='rent_unit', verbose_name='Объект аренды')
    warehouse = models.ForeignKey(Warehouse, related_name='warehouse', verbose_name='Склад')
    price = models.FloatField(verbose_name='Цена')
    period = models.ForeignKey(PricePeriod, related_name='period', verbose_name='Период')

    def __str__(self):
        return self.price

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
        db_table = 'prices'

