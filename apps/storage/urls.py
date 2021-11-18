from django.urls import path
from .views import map_view, calculator, user_orders

urlpatterns = [
    path('', map_view, name='main_page'),
    path('storage/<int:category_id>', calculator, name='calculator'),
    path('user-orders/<int:user_id>', user_orders, name='user_orders')
]