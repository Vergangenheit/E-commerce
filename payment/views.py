import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from .secrets import stripe_publishable_key as stripe_key
import stripe
from django.views.decorators.csrf import csrf_exempt
from stripe import PaymentIntent
from basket.basket import Basket
import json
from orders.views import payment_confirmation
# Create your views here.
@login_required
def BasketView(request: HttpRequest) -> HttpResponse:
    basket = Basket(request)
    total = str(basket.get_total_price())
    total: str = total.replace('.', '')

    stripe.api_key = stripe_key
    # build an intent
    intent: PaymentIntent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )
    return render(request, 'payment/home.html', {'client_secret': intent.client_secret})

@csrf_exempt
def stripe_webhook(request: HttpRequest) -> HttpResponse:
    payload: bytes = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)
    
    # handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)
    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

def order_placed(request: HttpRequest) -> HttpResponse:
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')

