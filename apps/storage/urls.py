from django.urls import path, include
from .views import main_page, get_calculator, user_orders, get_order, get_unit_price

urlpatterns = [
    path('storage/<int:category_id>/<int:warehouse_id>/', get_calculator, name='calculator'),
    path('order/<int:id>/', get_order, name='order'),
    path('order/<int:order_id>/payment/', include('apps.payment.urls')),
    path('user-orders/<int:user_id>', user_orders, name='user_orders'),
    path('price/', get_unit_price, name='get_unit_price'),
    path('', main_page, name='main_page'),
    
]