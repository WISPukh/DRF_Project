import pytest


class TestCart:
    endpoint = '/api/cart/'

    @pytest.mark.django_db
    def test_retrieve(self, auto_login_user):
        client, user = auto_login_user()

        # add product to cart
        product = client.get('/api/products/1/').data
        client.post(f"/api/products/{product.get('id')}/add_to_cart/", {"quantity": 3}, format='json')

        # check the cart
        response = client.get(self.endpoint)
        cart = response.data[0].get('cart')[0]

        assert response.status_code == 200
        assert response.data[0].get('customer_id') == user.id
        assert cart.get('product_id') == product.get('id')
        assert cart.get('quantity') == 3
        assert response.data[0].get('total_price') == product.get('price') * 3

    @pytest.mark.django_db
    def test_change_cart(self, auto_login_user):
        client, user = auto_login_user()

        client.post(f"/api/products/1/add_to_cart/", {"quantity": 1}, format='json')
        client.post(f"/api/products/2/add_to_cart/", {"quantity": 2}, format='json')
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
        response = client.patch(self.endpoint + '2/', data_to_change, format='json')

        assert response.status_code == 200
        assert response.data.get('cart') == data_to_change['cart']

    @pytest.mark.django_db
    def test_make_order(self, auto_login_user):
        client, user = auto_login_user()
        make_order_data = {
            'city': 'something',
            'address': 'another'
        }

        client.post(f"/api/products/1/add_to_cart/", {"quantity": 1}, format='json')
        client.post(f"/api/products/2/add_to_cart/", {"quantity": 2}, format='json')
        response = client.post(self.endpoint + '3/', make_order_data, format='json')
        order_history = client.get('/api/orders/history/')

        assert response.status_code == 200
        assert client.get(self.endpoint).data == []  # после составления заказа, корзина пуста
        assert order_history.status_code == 200
        assert order_history.data != []

    @pytest.mark.django_db
    def test_unfilled_order(self, auto_login_user):
        client, user = auto_login_user()
        make_order_data = {
            'city': '',
            'address': ''
        }

        client.post(f"/api/products/1/add_to_cart/", {"quantity": 1}, format='json')
        client.post(f"/api/products/2/add_to_cart/", {"quantity": 2}, format='json')
        response = client.post(self.endpoint + '3/', make_order_data, format='json')

        assert response.status_code == 400
        assert response.content == b'"{\\"error\\": \\"You can not make an order without city or address\\"}"'

    @pytest.mark.django_db
    def test_incorrect_values_order(self, auto_login_user):
        client, user = auto_login_user()
        make_order_data = {
            'city': 'something',
            'address': 'another'
        }

        client.post(f"/api/products/1/add_to_cart/", {"quantity": 88888}, format='json')
        client.post(f"/api/products/2/add_to_cart/", {"quantity": 99999}, format='json')
        response = client.post(self.endpoint + '3/', make_order_data, format='json')

        assert response.status_code == 400
        assert response.content == b'"{\\"error\\": \\"incorrect amount of products in cart\\"}"'

    @pytest.mark.django_db
    def test_negative_values_order(self, auto_login_user):
        client, user = auto_login_user()
        make_order_data = {
            'city': 'something',
            'address': 'another'
        }

        client.post(f"/api/products/1/add_to_cart/", {"quantity": -5}, format='json')
        client.post(f"/api/products/2/add_to_cart/", {"quantity": -99999}, format='json')
        response = client.post(self.endpoint + '3/', make_order_data, format='json')

        assert response.status_code == 400
        assert response.content == b'"{\\"error\\": \\"incorrect amount of products in cart\\"}"'
