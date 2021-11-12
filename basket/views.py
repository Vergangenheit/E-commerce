from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from .basket import Basket
from django.shortcuts import get_object_or_404
from store.models import Product
from typing import Optional
from decimal import Decimal

# Create your views here.
def basket_summary(request: HttpRequest) -> HttpResponse:
    basket = Basket(request)
    return render(request, 'basket/summary.html', {'basket': basket})

def basket_add(request: HttpRequest) -> Optional[JsonResponse]:
    # let's grab the session data
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        # get the product id
        product_id: int = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product: Product = get_object_or_404(Product, id=product_id)
        # save it to our session
        basket.add(product=product, qty=product_qty)

        basketqty = basket.__len__()
        # build a response updating quantity and total price
        response = JsonResponse({'qty': basketqty})

        return response

def basket_delete(request: HttpRequest) -> Optional[JsonResponse]:
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response

def basket_update(request: HttpRequest) -> Optional[JsonResponse]:
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty: int = basket.__len__()
        baskettotal: Decimal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
