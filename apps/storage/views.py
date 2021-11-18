from django.shortcuts import render
from django.http import HttpResponseRedirect

def map_view(request):
    warehouses = {
        'Склад №1': [[55.705546, 37.479194], 'Краткое описание №1'],
        'Склад №2': [[55.654628, 37.530185], 'Краткое описание №2'],
        'Склад №3': [[55.673229, 37.781720], 'Краткое описание №3'],
        'Склад №4': [[55.827428, 37.622504], 'Краткое описание №4'],
    }

    return render(request, 'map.html', context={'warehouses': warehouses})


def calculator(request, category_id):
    return HttpResponseRedirect('/')


def user_orders(request, user_id):
    return HttpResponseRedirect('/')
