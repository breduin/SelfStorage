"""
Источник: https://pythonpip.ru/osnovy/geopy-python
"""
from decimal import *
from geopy.distance import great_circle as GC
from .models import Warehouse
from django.shortcuts import render
   

def get_nearest_warehouse(request, latitude, longitude):

    user_position = (Decimal(latitude), Decimal(longitude))

    warehouses = Warehouse.objects.all()

    w_distances = {}
    for w in warehouses:
        w_coords = (w.latitude, w.longitude)
        distance = GC(user_position, w_coords).km
        w_distances[distance] = w
        print(w.title, distance)
    
    distances = w_distances.keys()
    min_distance = min(distances)
    nearest_warehouse = w_distances[min_distance]

    context = {
        'warehouse': nearest_warehouse,
        'distance': min_distance,

    }

    return render(request, 'nearest_warehouse.html', context)