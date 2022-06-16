from django.urls import path
from payments.views import PaymentSuccessView, CancelView, CreateCheckoutSessionView
app_name='payments'

urlpatterns=[

    path('api/checkout-session/', CreateCheckoutSessionView.as_view(), name='checkout_session'),

    path('cancel/', CancelView.as_view(), name='cancel'),
    path('successpage/', PaymentSuccessView.as_view(), name='successpage'),
]