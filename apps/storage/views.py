from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from django.urls import reverse
from datetime import date

from .models import Warehouse, Price
from .forms import OrderUnitForm, OrderForm
from django.views.generic import TemplateView


def main_page(request):
    warehouses = Warehouse.objects.all()
    
    warehouses_for_template = {}
    for w in warehouses:
        warehouses_for_template[w.title] = [[w.latitude, w.longitude], w.description]
        print(w.longitude, w.latitude)

    return render(request, 'main_page.html', context={
                                        'warehouses': warehouses,
                                        'YANDEX_MAPS_API_KEY': settings.YANDEX_MAPS_API_KEY,
                                        }
                 )


def get_calculator(request, category_id, warehouse_id=1):

    if request.method == 'POST':
        order_unit_form = OrderUnitForm(request.POST)
        print(request.POST)
        if order_unit_form.is_valid():
            order_unit = order_unit_form.save(commit=False)
            # FIXME Добавить ID warehouse (переставить поля в модели)
            unit_id = order_unit.unit.id
            warehouse_id = 1
            duration = order_unit.rent_duration
            # находим единицу измерения периода, week или month
            period_id = 3 if 'week' in duration else 4
            
            quantity = order_unit.quantity
            unit_price = Price.objects.get(unit__id=unit_id, 
                                           warehouse__id=warehouse_id, 
                                           period__id=period_id,
                                           ).price
            order_unit.price = unit_price * quantity
            print('OrderUnit:', order_unit)
            order_unit.save()
            return HttpResponseRedirect(reverse('order'))
    else:
        kwargs = {'category_id': category_id}
        today = date.today()
        initial_values = {
            'quantity': 1,
            'rent_start': today.strftime("%Y-%m-%d"), 
        }
        order_unit_form = OrderUnitForm(category_id=category_id, initial=initial_values)
        # FIXME указать initial_price для начальных значений формы
        context = {
            'order_unit_form': order_unit_form,
            'initial_price': 10,
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
def get_unit_price(request):
    """
    Возвращает стоимость аренды объекта в зависимости 
    от количества, склада и срока аренды.
    """
    unit_id = request.GET.get('unit_id', None)
    warehouse_id = request.GET.get('warehouse_id', None)
    duration = request.GET.get('duration', None)
    quantity = request.GET.get('quantity', 1)
    price = 100 * int(quantity)
    price_for_template = {'price': price}
    return JsonResponse(price_for_template)