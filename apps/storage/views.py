from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from .models import Warehouse


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


def calculator(request, category_id):
    return HttpResponseRedirect('/')


def user_orders(request, user_id):
    return HttpResponseRedirect('/')
