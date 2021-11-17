import stripe
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.conf import settings


def make_payment(request):
    stripe.api_key = settings.STRIPE_PUBLISHABLE_KEY

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'T-shirt',
                },
                'unit_amount': 2000,
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
