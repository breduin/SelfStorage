from django.urls import path
from . import views

app_name = "apps.payment"

urlpatterns = [
    path('', views.make_payment, name='make_payment'),
    path('success/', views.pay_success, name='successed_payment'),
    path('cancelled/', views.CancelledView.as_view(), name='cancelled_payment'),
]