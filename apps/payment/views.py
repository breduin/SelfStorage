import stripe
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.conf import settings
from apps.storage.models import Order, OrderUnit
from django.db.models import Avg, Count, Min, Sum


def make_payment(request, order_id):
    stripe.api_key = settings.STRIPE_PUBLISHABLE_KEY

    order = Order.objects\
        .annotate(order_price=Sum('rent_order__price'))\
        .get(id=order_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': f'Ваш заказ № {order_id}',
                },
                'unit_amount': int(order.order_price)*100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=f'http://127.0.0.1:8000/order/{order_id}/payment/success/',
        cancel_url=f'http://127.0.0.1:8000/order/{order_id}/',
    )

    return redirect(session.url, code=303)


def pay_success(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'ORDER'
    order.save()
    return render(request, "success.html")


class CancelledView(TemplateView):
    template_name = 'cancelled.html'
