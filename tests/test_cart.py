import pytest
from django.urls import reverse_lazy
from rest_framework.test import APIClient


class TestCart:
    endpoint = reverse_lazy('cart-list')

    @pytest.mark.django_db
    def test_retrieve(self, auto_login_user):
        client, user = auto_login_user()

        self.add_product_to_cart(client, 1, 3)

        response = client.get(self.endpoint)
        cart = response.data[0].get('cart')[0]

        assert response.status_code == 200
        assert response.data[0].get('customer_id') == user.id
        assert cart.get('product_id') == 1
        assert cart.get('quantity') == 3

    @pytest.mark.django_db
    def test_change_cart(self, auto_login_user):
        client, user = auto_login_user()
        self.add_product_to_cart(client, 1, 1)
        self.add_product_to_cart(client, 2, 2)
        data_to_change = {
            "cart": [
                {
                    "product_id": 3,
                    "quantity": 3
                },
                {
                    "product_id": 4,
                    "quantity": 4
                }
            ]
        }

        response = client.patch(f'{self.endpoint}2/', data_to_change, format='json')

        assert response.status_code == 200
        assert response.data.get('cart') == data_to_change['cart']

    @pytest.mark.django_db
    def test_make_order(self, auto_login_user):
        client, user = auto_login_user()
        self.add_product_to_cart(client, 1, 2)
        order_data = {
            'city': 'something',
            'address': 'another'
        }

        response = client.post(self.endpoint, order_data, format='json')
        order_history = client.get(reverse_lazy('orders-list'))

        assert response.status_code == 200
        assert client.get(self.endpoint).data == []  # после составления заказа, корзина пуста
        assert order_history.status_code == 200
        assert order_history.data != []

    @pytest.mark.parametrize(
        'city,address,quantity_1,quantity_2,expected',
        [
            ('', '', 1, 2, b'"{\\"error\\": \\"You can not make an order without city or address\\"}"'),
            ('city', 'address', 88888, 99999, b'"{\\"error\\": \\"incorrect amount of products in cart\\"}"'),
            ('city', 'address', -5, -999999, b'"{\\"error\\": \\"incorrect amount of products in cart\\"}"')
        ]
    )
    def test_make_incorrect_order(self, auto_login_user, city, address, quantity_1, quantity_2, expected):
        client, user = auto_login_user()
        order_data = {
            'city': city,
            'address': address
        }

        self.add_product_to_cart(client, 1, quantity_1)
        self.add_product_to_cart(client, 2, quantity_2)
        response = client.post(self.endpoint, order_data, format='json')

        assert response.status_code == 400
        assert response.content == expected

    @staticmethod
    def add_product_to_cart(client: APIClient, product_id: int, quantity: int) -> None:
        client.post(reverse_lazy('add_to_cart-add-to-cart', args=[product_id]), {"quantity": quantity}, format='json')
