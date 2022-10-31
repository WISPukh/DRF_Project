from unittest import TestCase

import pytest
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from parameterized import parameterized

from cart.models import Order
from cart.services import CartActionsService
from shop.models import Mixer, Product
from users.models import User


class CartUnitTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='puhoff.ol@yandex.ru', password='123123qwer')

        mixer_data = {
            'name': 'mixer',
            'description': 'whatever',
            'price': 999,
            'in_stock': 25,
            'content_type': ContentType.objects.get(model='mixer'),
            'mixer_type': 'strong god damn it'
        }
        self.product = Mixer.objects.create(**mixer_data)
        self.add_products(product_id=1)
        self.order = self.add_products(product_id=2, quantity=2)

    @pytest.mark.django_db
    def test_add_product_to_cart(self):
        order = self.add_products(product_id=4, quantity=4)
        cart_data = order.orderitem_set.all().values().last()

        self.assertNotEqual(cart_data, [])
        self.assertEqual(cart_data['product_id_id'], 4)
        self.assertEqual(cart_data['quantity'], 4)
        self.assertEqual(order.calculated_total_amount, 7)  # 3 in setUp; 4 in this function

    @pytest.mark.django_db
    def test_make_order(self):
        payload = {
            'city': 'rnd',
            'address': 'true and valid address'
        }

        service = CartActionsService(
            user=self.user,
            order=self.order,
            request_data=payload
        )
        normal_order = service.make_order()

        self.assertEqual(normal_order.status, 'CREATED')
        self.assertEqual(normal_order.city, payload['city'])
        self.assertEqual(normal_order.address, payload['address'])

    @parameterized.expand([
        ['', '', 1],
        ['city', 'address', 88888],
        ['city', 'address', -5]
    ])
    @pytest.mark.django_db
    def test_incorrect_values_order(self, city, address, quantity):
        payload = {
            'city': city,
            'address': address
        }

        service = CartActionsService(
            user=self.user,
            order=self.add_products(product_id=1, quantity=quantity),
            request_data=payload
        )
        order = service.make_order()

        self.assertEqual(order.status_code, 400)
        self.assertIsInstance(order, HttpResponse)

    @pytest.mark.django_db
    def test_change_products_in_cart(self):
        payload = {
            'cart': [
                {
                    'product_id': 2,
                    'quantity': 5
                },
                {
                    'product_id': 3,
                    'quantity': 3
                }
            ]
        }

        service = CartActionsService(user=self.user, product=self.product, request_data=payload, order=self.order)
        order = service.change_products_in_cart()
        cart_data = list(order.orderitem_set.all().values('product_id', 'quantity'))

        self.assertEqual(cart_data, payload['cart'])

    def add_products(self, product_id: int, quantity: int = 1) -> Order:
        payload = {
            'product_id': product_id,
            'quantity': quantity
        }
        product = Product.objects.get(pk=product_id)
        service = CartActionsService(user=self.user, product=product, request_data=payload)
        order = service.add_product_to_cart()
        order.save()

        return order
