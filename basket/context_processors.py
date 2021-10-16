from .basket import Basket
from django.http import HttpRequest


def basket(request: HttpRequest):
    return {'basket': Basket(request)}
