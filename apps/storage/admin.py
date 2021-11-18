from django.contrib import admin
from .models import Warehouse, Unit, Price, Category, UnitMeasurement\
    , PricePeriod, BaseStepPrice, Order, OrderUnit

admin.site.register(Warehouse)

admin.site.register(Unit)

admin.site.register(Price)

admin.site.register(Category)

admin.site.register(UnitMeasurement)

admin.site.register(PricePeriod)

admin.site.register(BaseStepPrice)
