import stripe
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.conf import settings
from apps.storage.models import Order


def make_payment(request, order_id):
    stripe.api_key = settings.STRIPE_PUBLISHABLE_KEY

    order = Order.objects.get(id=order_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'rub',
                'product_data': {
                    'name': order.access_code,
                },
                'unit_amount': order.get_sum()*100,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/payment/success',
        cancel_url='http://localhost:8000/',
    )

    return redirect(session.url, code=303)


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelledView(TemplateView):
    template_name = 'cancelled.html'
