import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse

# Create your views here.
@login_required
def BasketView(request: HttpRequest) -> HttpResponse:
    return render(request, 'payment/home.html')