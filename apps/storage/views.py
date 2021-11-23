import re
import json
from datetime import date

from django.db.models import Sum
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.urls import reverse
from django.db import transaction, models

from .models import Warehouse, Price, Unit, Order, OrderUnit, BaseCategoryPrice
from apps.users.models import User
from .forms import OrderUnitForm
from .help_functions import get_random_string


def main_page(request):
    warehouses = Warehouse.objects.all()
    
    warehouses_for_template = {}
    for w in warehouses:
        warehouses_for_template[w.title] = [[w.latitude, w.longitude], w.description]

    return render(request, 'main_page.html', context={
                                        'warehouses': warehouses,
                                        'YANDEX_MAPS_API_KEY': settings.YANDEX_MAPS_API_KEY,
                                        }
                 )


@transaction.atomic
def get_calculator(request, category_id, warehouse_id=1):

    if request.method == 'POST':
        order_unit_form = OrderUnitForm(request.POST)
        if order_unit_form.is_valid():

            order_unit = order_unit_form.save(commit=False)
            
            unit_id = order_unit.unit.id
            
            warehouse_id = order_unit.warehouse.id
            
            duration = order_unit.rent_duration
            
            quantity = order_unit.quantity

            get_price = json.loads(get_unit_price(request,
                                                  unit_id=unit_id,
                                                  warehouse_id=warehouse_id,
                                                  duration=duration,
                                                  quantity=quantity
                                                  ).content
                                   )

            order_unit.price = get_price['price']

            # Создание Order
            
            access_code = get_random_string()
            if request.user.is_authenticated:
                order = Order.objects.create(access_code=access_code,
                                             user=request.user,
                                             )
                order_unit.order_id = order.id

                order_unit.save()

                return HttpResponseRedirect(reverse('order', args=[order.id]))

            else:
                order = Order.objects.create(access_code=access_code,
                                             user=User.objects.get(id=1),
                                             )

                order_unit.order_id = order.id

                order_unit.save()

                if 'have_account' in request.POST:
                    return HttpResponseRedirect(reverse('login', args=[order.id]))
                elif 'want_account' in request.POST:
                    return HttpResponseRedirect(reverse('register', args=[order.id]))

    else:
        kwargs = {'category_id': category_id}
        
        today = date.today()
        initial_warehouse = warehouse_id
        initial_unit = Unit.objects.filter(category__id=category_id).first()
        initial_quantity = 1
        initial_duration = '1month'

        initial_values = {
            'quantity': initial_quantity,
            'rent_start': today.strftime("%Y-%m-%d"), 
            'unit': initial_unit.id,
            'rent_duration': initial_duration,
            'warehouse': initial_warehouse,
        }
        order_unit_form = OrderUnitForm(category_id=category_id, initial=initial_values)
        order_unit_form.fields['unit'].queryset = Unit.objects.filter(category__id=category_id)
        
        # initial_price для начальных значений формы
        get_price = json.loads(get_unit_price(request, 
                        unit_id=initial_unit.id, 
                        warehouse_id=warehouse_id, 
                        duration=initial_duration, 
                        quantity=initial_quantity
                                              ).content
                               )

        context = {
            'order_unit_form': order_unit_form,
            'initial_price': get_price['price'],
            'category': category_id,
                   }
        return render(request, 'add_orderunit.html', context)

    # возвращает, если форма невалидна
    context = {
        'order_unit_form': OrderUnitForm(request.POST),
        'initial_price': 10,
        'category': category_id,
                }

    return render(request, 'add_orderunit.html', context)


def get_order(request, id):

    order = Order.objects.get(id=id)
    order_units = OrderUnit.objects.filter(order=order)
    context = {
        'order_units': order_units,
        'order_id': order.id,
    }

    return render(request, 'order_confirmation.html', context)


def get_user_orders(request):

    orders = Order.objects \
        .annotate(order_price=Sum('rent_order__price')) \
        .filter(user__id=request.user.id)
    context = {'orders': orders}
    return render(request, 'user_orders.html', context)


def get_unit_price(request, unit_id=None, warehouse_id=None, duration=None, quantity=None):
    """
    Возвращает стоимость аренды объекта в зависимости 
    от количества, склада и срока аренды.
    """
    unit_id = unit_id or request.GET.get('unit_id', None)
    warehouse_id = warehouse_id or request.GET.get('warehouse_id', None)
    duration = duration or request.GET.get('duration', None)
    quantity = quantity or request.GET.get('quantity', 1)
    
    # находим единицу измерения периода, week или month
    period_id = 3 if 'week' in duration else 4

    # находим количество периодов, т.е. срок аренды
    number_of_periods = int(re.match(r'\d{1,2}', duration).group(0))
    
    unit_price = Price.objects.get(unit__id=unit_id, 
                                   warehouse__id=warehouse_id, 
                                   period__id=period_id,
                                   ).price                                    
    price = unit_price * int(quantity) * number_of_periods
    unit = Unit.objects.get(id=unit_id)
    try:
        base_price = BaseCategoryPrice.objects.get(category=unit.category.id, warehouse=warehouse_id).price
    except BaseCategoryPrice.DoesNotExist:
        base_price = 0 

    price += base_price
    

    price_for_template = {'price': price}
    return JsonResponse(price_for_template)
