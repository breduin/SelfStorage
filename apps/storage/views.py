import re
import json
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.urls import reverse
from datetime import date

from .models import Warehouse, Price, Unit
from .forms import OrderUnitForm, OrderForm
from django.views.generic import TemplateView


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


def get_calculator(request, category_id, warehouse_id=1):

    if request.method == 'POST':
        order_unit_form = OrderUnitForm(request.POST)
        if order_unit_form.is_valid():
            order_unit = order_unit_form.save(commit=False)
            
            unit_id = order_unit.unit.id
            
            # FIXME Добавить ID warehouse (переставить поля в модели)
            warehouse_id = 1
            
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
            order_unit.save()
            return HttpResponseRedirect(reverse('order'))
    else:
        kwargs = {'category_id': category_id}
        
        today = date.today()
        initial_unit = Unit.objects.filter(category__id=category_id).first()
        initial_quantity = 1
        initial_duration = '1month'

        initial_values = {
            'quantity': initial_quantity,
            'rent_start': today.strftime("%Y-%m-%d"), 
            'unit': initial_unit.id,
            'rent_duration': initial_duration,
        }
        order_unit_form = OrderUnitForm(category_id=category_id, initial=initial_values)
        
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
        return render(request, 'add_orderunit.html', context )

    # возвращает, если форма невалидна
    # FIXME указать initial_price для формы, которая вернулась с ошибкой
    context = {
        'order_unit_form': OrderUnitForm(request.POST),
        'initial_price': 10,
        'category': category_id,
                }

    return render(request, 'add_orderunit.html', context)

def make_order(request, category_id, warehouse_id=1):

    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            # return redirect('/')
    else:
        order_form = OrderForm()
        return render(request,
                      'add_order.html',
                      {'order_form': order_form}
                      )


class OrderConfirmation(TemplateView):
    template_name = 'order_confirmation.html'


def user_orders(request, user_id):
    return HttpResponseRedirect('/')


# TODO дописать функцию для AJAX-запроса
def get_unit_price(request, unit_id=None, warehouse_id=None, duration=None, quantity=None):
    """
    Возвращает стоимость аренды объекта в зависимости 
    от количества, склада и срока аренды.
    """
    unit_id = unit_id or request.GET.get('unit_id', None)
    warehouse_id = warehouse_id or request.GET.get('warehouse_id', None)
    warehouse_id = 1
    duration = duration or request.GET.get('duration', None)
    quantity = quantity or request.GET.get('quantity', 1)
    
    # находим единицу измерения периода, week или month
    period_id = 3 if 'week' in duration else 4

    # находим количество периодов, т.е. срок аренды
    # ВНИМАНИЕ, ИЗВРАТ! Слабонервным не смотреть.
    number_of_periods = int(re.match(r'\d{1,2}', duration).group(0))
    
    unit_price = Price.objects.get(unit__id=unit_id, 
                                    warehouse__id=warehouse_id, 
                                    period__id=period_id,
                                    ).price
    price = unit_price * int(quantity) * number_of_periods    

    price_for_template = {'price': price}
    return JsonResponse(price_for_template)