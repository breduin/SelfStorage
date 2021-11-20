from django.urls import path
from . import views

app_name = "apps.payment"

urlpatterns = [
    path('<int:order_id>', views.make_payment, name='make_payment'),
    path('<int:id>/success/', views.SuccessView.as_view(), name='successed_payment'),
    path('<int:id>/cancelled/', views.CancelledView.as_view(), name='cancelled_payment'),
]