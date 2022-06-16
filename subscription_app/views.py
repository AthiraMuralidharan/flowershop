from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer, CustomerStatus
import stripe

# Create your views here.
stripe.api_key = "sk_test_51L0garSIjRsqsoNHCiAx6iokXzrzlqH9U4hf1HTZCcAAgyfC6Edj8SWTtGW2rbndzx5br09zGcMgNdvIVBiJn4LS008wXPRAwE"


def index(request):
    return render(request, 'membership/index.html')


# @login_required
def settings(request):
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    return render(request, 'registration/settings.html', {'membership': membership,
                                                      'cancel_at_period_end': cancel_at_period_end})



def join(request):
    return render(request, 'membership/join.html')


def success(request):
    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'], )
        customer = Customer()
        # customer = Customer.objects.get(user=request.user, stripeid =session.customer, membership = True, cancel_at_period_end = False, stripe_subscription_id = session.subscription)
        # customer = Customer.objects.get(user=request.user)
        customer.user = request.user
        customer.stripeid = session.customer
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = session.subscription

        CustomerStatus.status = 'active'
        # customer.save()
        # print(customer)
        # customer = Customer.objects.create(user = request.user, stripeid =session.customer, membership = True, cancel_at_period_end = False, stripe_subscription_id = session.subscription )
        customer.save()
       

    return render(request, 'membership/success.html')


def canceled(request):
    return render(request, 'membership/cancel.html')


# @login_required
def checkout(request):
    try:
        if request.user.customer.membership:
            return redirect('settings')
    except Customer.DoesNotExist:
        pass

    if request.method == 'POST':
        pass
    else:
        membership = 'monthly'
        final_dollar = 1000
        membership_id = 'price_1L0kmASIjRsqsoNHShe0ZAT8'
        if request.method == 'GET' and 'membership' in request.GET:
            if request.GET['membership'] == 'yearly':
                membership = 'yearly'
                membership_id = 'price_1L0kmASIjRsqsoNH1wWGyFgd'
                final_dollar = 5000

        # Create Strip Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=request.user.email,
            line_items=[{
                'price': membership_id,
                'quantity': 1,
            }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url='http://127.0.0.1:8000/subscription_app/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/subscription_app/canceled',
        )

        return render(request, 'membership/checkout.html', {'final_dollar': final_dollar, 'session_id': session.id})

def Pausepayment(request):
    stripe.Subscription.modify(
    request.user.customer.stripe_subscription_id,
    pause_collection={
        'behavior': 'mark_uncollectible',
    },
    )
    Customer.status = 'pause'
    # return HttpResponse('Subscription paused')
    return render(request,'membership/pause.html')

def Resumepayment(request):
    stripe.Subscription.modify(
        request.user.customer.stripe_subscription_id,
        pause_collection='',
    )
    Customer.status = 'active'
    # return HttpResponse("Resumed Successfully")
    return render(request, 'membership/resume.html')

def delete(request):
    # Permanantly delete Subscription id
    stripe.Subscription.delete(stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)),
    # Permanantly delete Subscription id, status, membership from Customer model
    v = Customer.objects.get(user=request.user).delete()
    customer = Customer.objects.create(user=request.user)

    # return HttpResponse("cancelled successfully")
    return render(request, 'membership/delete.html')

def Updatesubscription(request):
    current_subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)

    # new plan
    stripe.Subscription.modify(
        request.user.customer.stripe_subscription_id,
        cancel_at_period_end=True,
        proration_behavior='create_prorations',
        # the new subscription
        items=[{
            'id': current_subscription['items'].data[0].id,
            # note if you have more than one Plan per Subscription, you'll need to improve this. This assumes one plan per sub.
            'deleted': True,

        }, {
            'plan': 'price_1L0kmASIjRsqsoNH1wWGyFgd'
        }]
    )
    # return HttpResponse('Subscription updated')
    return render(request, 'membership/update.html')