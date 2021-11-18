from django.urls import path
from .views import main_page, calculator, user_orders, make_order

urlpatterns = [
    path('storage/<int:category_id>/<int:warehouse_id>/', calculator, name='calculator'),
    path('storage/order/<int:category_id>/<int:warehouse_id>/', make_order, name='order'),
    path('user-orders/<int:user_id>', user_orders, name='user_orders'),
    path('', main_page, name='main_page'),
]