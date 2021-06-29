from django.http import HttpRequest
from typing import Dict
from .models import Category


def categories(request: HttpRequest) -> Dict:
    return {
        'categories': Category.objects.all()
    }
