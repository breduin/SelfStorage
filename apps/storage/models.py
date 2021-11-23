from datetime import timedelta
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.conf import settings
from django.utils import timezone
from .help_functions import get_period_and_number_duration
from .validators import lat_validators, lng_validators


class Warehouse(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название склада')
    description = models.TextField(verbose_name='Подробное описание склада')
    address = models.CharField(max_length=200, unique=True,
                               verbose_name='Адрес склада')
    phone = PhoneNumberField(
        verbose_name='Телефонный номер склада',
        help_text='Введите номер телефона, например, +79999999999'
    )
    latitude = models.FloatField(validators=lat_validators,
                                 verbose_name='Широта', )
    longitude = models.FloatField(validators=lng_validators,
                                  verbose_name='Долгота')
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.title

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
    measurement = models.ForeignKey(UnitMeasurement,
                                    on_delete=models.CASCADE,
                                    related_name='mes_name',
                                    verbose_name='Единица измерения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'categories'


class PricePeriod(models.Model):
    duration = models.CharField(max_length=100, verbose_name='Единица времени')

    def __str__(self):
        return self.duration

    class Meta:
        verbose_name = 'Базовое время аренды'
        verbose_name_plural = 'Базовое время аренды'
        db_table = 'price_periods'


class BaseCategoryPrice(models.Model):
    category = models.ForeignKey(Category, 
                                 on_delete=models.CASCADE, 
                                 related_name='price', 
                                 verbose_name='Категория'
                                 )
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,
                                  related_name='main_storage',
                                  verbose_name='Склад')
    price = models.FloatField(verbose_name='Базовая цена')

    def __str__(self):
        return f"{self.category} | {self.warehouse.title} | {str(self.price)}"

    class Meta:
        verbose_name = 'Базовая цена'
        verbose_name_plural = 'Базовые цены'
        unique_together = ['category', 'warehouse']


class Unit(models.Model):
    name = models.CharField(max_length=200, verbose_name='Объект аренды')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='category',
                                 verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объект аренды'
        verbose_name_plural = 'Объекты аренды'
        db_table = 'units'


class Price(models.Model):
    unit = models.ForeignKey(Unit,
                             on_delete=models.CASCADE,
                             related_name='rent_unit',
                             verbose_name='Объект аренды')
    warehouse = models.ForeignKey(Warehouse,
                                  on_delete=models.CASCADE,
                                  related_name='storage',
                                  verbose_name='Склад')
    price = models.FloatField(verbose_name='Цена')
    period = models.ForeignKey(PricePeriod,
                               on_delete=models.CASCADE,
                               related_name='period',
                               verbose_name='Период')

    def __str__(self):
        return f"{self.unit.name}|{self.warehouse.title}|{self.period}|{str(self.price)}"

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
        db_table = 'prices'


class Order(models.Model):

    STATUS_CHOICES = [
        ('PREORDER', 'Не оплачен'),
        ('ORDER', 'Оплачен'),
        ('DONE', 'Завершён'),
    ]

    status = models.CharField('Статус заказа',
                              max_length=10,
                              choices=STATUS_CHOICES,
                              default='PREORDER'
                              )
    access_code = models.CharField(max_length=50, 
                                   unique=True, 
                                   verbose_name='Код доступа'
                                   )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             editable=False
                             )

    def get_sum(self):
        # FIXME
        pass

    def __str__(self):
        return f"№ {self.id} | {self.user.username} | {self.get_status_display()}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'orders'


class OrderUnit(models.Model):

    DURATION_CHOICES = [
        ('1week', '1 неделя'),
        ('2weeks', '2 недели'),
        ('3weeks', '3 недели'),
        ('1month', '1 месяц'),
        ('2months', '2 месяца'),
        ('3months', '3 месяца'),
        ('4months', '4 месяца'),
        ('5months', '5 месяцев'),
        ('6months', '6 месяцев'),
        ('7months', '7 месяцев'),
        ('8months', '8 месяцев'),
        ('9months', '9 месяцев'),
        ('10months', '10 месяцев'),
        ('11months', '11 месяцев'),
        ('12months', '12 месяцев'),
    ]

    warehouse = models.ForeignKey(Warehouse,
                                  null=True,
                                  on_delete=models.SET_NULL,
                                  related_name='warehouse',
                                  verbose_name='Склад'
                                  )
    unit = models.ForeignKey(Unit,
                             on_delete=models.DO_NOTHING,
                             related_name='unit',
                             verbose_name='Объект аренды')
    order = models.ForeignKey(Order,
                              on_delete=models.DO_NOTHING,
                              related_name='rent_order',
                              verbose_name='Основной заказ',
                              editable=False
                              )
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', 
                                                default=1
                                                )
    rent_start = models.DateField(verbose_name='Дата начала аренды',
                                  null=True, 
                                  default=timezone.now
                                  )
    rent_duration = models.CharField('Длительность аренды', 
                                      max_length=10, 
                                      choices=DURATION_CHOICES, 
                                      default='1month')
    price = models.FloatField(verbose_name='Цена', 
                              editable=False, 
                              null=True,                               
                              )

    @property
    def rent_end(self):
        days_quantity_in_period = {
                                    3: 7, # неделя
                                    4: 30, # месяц
                                  }

        period_id, number_of_periods = get_period_and_number_duration(self.rent_duration)
        delta = timedelta(days=days_quantity_in_period[period_id] * number_of_periods)
        return self.rent_start + delta
