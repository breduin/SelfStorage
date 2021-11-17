from django.urls import path
from . import views

app_name = "apps.payment"

urlpatterns = [
    path('', views.make_payment),
    path('success/', views.SuccessView.as_view()),
    path('cancelled/', views.CancelledView.as_view()),
]