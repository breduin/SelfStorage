from django.urls import path, include
from .views import main_page, get_calculator, get_user_orders\
    , get_order, get_unit_price
from .geolocation import get_nearest_warehouse

urlpatterns = [
    path('storage/<int:category_id>/<int:warehouse_id>/',
         get_calculator, name='calculator'),
    path('order/<int:id>/', get_order, name='order'),
    path('order/<int:order_id>/payment/', include('apps.payment.urls')),
    path('user-orders/', get_user_orders, name='user_orders'),
    path('price/', get_unit_price, name='get_unit_price'),
    path('nearest-warehouse/<str:latitude>/<str:longitude>',
         get_nearest_warehouse, name='nearest_warehouse'),

    path('', main_page, name='main_page'),
    
]