from django.http import HttpRequest
from django.contrib.sessions.backends.base import SessionBase
from store.models import Product
from typing import Iterator, Sequence, Dict
from django.db.models import QuerySet
from decimal import Decimal
import re


class Basket():
    """A basket class, providing some default behaviours that can be inherited or overrided, as necessary"""

    def __init__(self, request: HttpRequest):

        self.session: SessionBase = request.session
        # first we need to check if the basket exists
        basket: Dict = self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product: Product, qty: int):
        """
        adding and updating the users basket session data
        """
        product_id = str(product.id)

        # check if item exist in their basket
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        # save it
        self.save()

    def __iter__(self) -> Iterator:
        """
        makes the class iterable
            Collect the product_id in the session data to query the database
        and return products
        """
        product_ids: Sequence = [i for i in self.basket.keys() if re.match('\d+', i)]
        products: QuerySet = Product.products.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            # get the basket and add some more data
            basket[str(product.id)]['product'] = product

        for item in [i for i in basket.values() if isinstance(i, dict)]:
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']

            yield item

    def __len__(self) -> int:
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values() if isinstance(item, dict))

    def get_total_price(self) -> Decimal:
        """returns the total basket price"""
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values()) 

    def delete(self, product: int) -> None:
        """deletes item from session data"""
        # find the item 
        product_id: str = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
        self.save()

    def update(self, product: int, qty: int) -> None:
        """
        Update values in session data
        """
        product_id: str = str(product)
        qty: int = qty
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty

        self.save()


    def save(self) -> None:
        """saves session"""
        self.session.modified = True

    def clear(self) -> None:
        del self.session['skey']
        self.save()
