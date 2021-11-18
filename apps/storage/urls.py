from django.urls import path
from .views import main_page, calculator, user_orders

urlpatterns = [
    path('storage/<int:category_id>', calculator, name='calculator'),
    path('user-orders/<int:user_id>', user_orders, name='user_orders'),
    path('', main_page, name='main_page'),
]