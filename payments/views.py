import json

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic
from django.views.generic import TemplateView


class PaymentSuccessView(TemplateView):
    template_name = "payments/successpage.html"


class CancelView(TemplateView):
    template_name = "payments/cancel.html"


stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(generic.View):
    def post(self, request, *args, **kwargs):
        # request_data = json.loads(request.body)
        price = request.session['total']
        checkout_session = stripe.checkout.Session.create(
            # customer_email=request_data['email'],
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(price * 100),
                        'product_data': {
                            'name': 'product.name'
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url="http://127.0.0.1:8000/payments/successpage/",
            cancel_url="http://127.0.0.1:8000/payments/cancel",
            # success_url=YOUR_DOMAIN + '/success.html',
            # cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
        return redirect(checkout_session.url, code=303)
        # return render(request, 'cart.html', {'sessionId': checkout_session.id})



