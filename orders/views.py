from django.shortcuts import render
from django.http.response import JsonResponse
from django.http.request import HttpRequest
from .models import OrderItem, Order
from basket.basket import Basket
from decimal import Decimal
from django.db.models import QuerySet

# Create your views here.
# catch the ajax request
def add(request: HttpRequest) -> JsonResponse:
    basket = Basket(request)
    if request.POST.get('action') == 'post':

        user_id: str = request.user.id
        order_key: str = request.POST.get('order_key')
        baskettotal: Decimal = basket.get_total_price()
        
        # check if the order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            # create the order
            order: Order = Order.objects.create(user_id=user_id, full_name='name', address1='add1',
                                address2='add2', total_paid=baskettotal, order_key=order_key)
            order_id: int = order.pk
            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])
        
        response = JsonResponse({'success': 'Return something'})
        return response

def payment_confirmation(data: str):
    Order.objects.filter(order_key=data).update(billing_status=True)

def user_orders(request: HttpRequest) -> QuerySet:
    user_id = request.user.id
    orders: QuerySet = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders




