from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from django.urls import reverse

from .models import Warehouse
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


def calculator(request, category_id, warehouse_id=1):

    if request.method == 'POST':
        order_unit_form = OrderUnitForm(request.POST)
        if order_unit_form.is_valid():
            order_unit = order_unit_form.save(commit=False)
            # FIXME Здесь надо цену посчитать
            return HttpResponseRedirect(reverse('order'))
    else:
        order_unit_form = OrderUnitForm()
        return render(request,
                      'add_orderunit.html',
                      {'order_unit_form': order_unit_form}
                      )


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
