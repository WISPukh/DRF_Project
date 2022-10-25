import pytest
from django.contrib.contenttypes.models import ContentType

from tests.factories import MixerFactory


class TestShop:
    endpoint = '/api/products/'

    @pytest.mark.django_db
    def test_create(self, auto_login_user):
        client, user = auto_login_user()
        create_data = {
            'name': 'mixer',
            'description': 'whatever',
            'price': 999,
            'in_stock': 15,
            'content_type': ContentType.objects.get(model='mixer').pk,
            'mixer_type': 'strong god damn it'
        }

        user.is_superuser = True
        user.save()
        response = client.post(self.endpoint, create_data, format='json')

        assert response.status_code == 201

    @pytest.mark.django_db
    def test_create_unauthorized(self, auto_login_user):
        client, user = auto_login_user()
        create_data = {
            'name': 'mixer',
            'description': 'whatever',
            'price': 999,
            'in_stock': 15,
            'content_type': ContentType.objects.get(model='mixer').pk,
            'mixer_type': 'strong god damn it'
        }

        response = client.post(self.endpoint, create_data, format='json')

        assert response.status_code == 403

    @pytest.mark.django_db
    def test_list(self, auto_login_user):
        client, user = auto_login_user()
        response = client.get(self.endpoint)

        assert response.status_code == 200
        assert response.data != []

    @pytest.mark.django_db
    def test_retrieve(self, auto_login_user):
        client, user = auto_login_user()
        response = client.get(self.endpoint + '1/')

        assert response.status_code == 200
        assert response.data.get('id') == 1

    @pytest.mark.django_db
    def test_delete(self, auto_login_user):
        client, user = auto_login_user()
        product = MixerFactory.create(content_type=ContentType.objects.get(model='mixer'))

        user.is_superuser = True
        user.save()
        response = client.delete(self.endpoint + f'{product.id}/')

        assert response.status_code == 204
        assert response.data != []

    @pytest.mark.django_db
    def test_delete_unauthorized(self, auto_login_user):
        client, user = auto_login_user()
        product = MixerFactory.create(content_type=ContentType.objects.get(model='mixer'))
        delete_response = client.delete(self.endpoint + f'{product.id}/')

        assert delete_response.status_code == 403

    @pytest.mark.django_db
    def test_add_product_to_cart(self, auto_login_user):
        client, user = auto_login_user()
        first_product_id = client.get(self.endpoint).data[0].get('id')

        response = client.post(f"{self.endpoint}{first_product_id}/add_to_cart/", {"quantity": 1}, format='json')

        assert response.data.get('cart')[0].get('product_id') == first_product_id
        assert response.data.get('cart')[0].get('quantity') == 1

    @pytest.mark.django_db
    def test_add_same_product_to_cart(self, auto_login_user):
        client, user = auto_login_user()
        first_product_id = client.get(self.endpoint).data[0].get('id')

        client.post(f"{self.endpoint}{first_product_id}/add_to_cart/", {"quantity": 1}, format='json')
        response = client.post(f"{self.endpoint}{first_product_id}/add_to_cart/", {"quantity": 1}, format='json')

        assert response.data.get('cart')[0].get('product_id') == first_product_id
        assert response.data.get('cart')[0].get('quantity') == 2

    @pytest.mark.django_db
    def test_add_multiple_products_to_cart(self, auto_login_user):
        client, user = auto_login_user()
        first_product_id = client.get(self.endpoint).data[0].get('id')
        second_product_id = client.get(self.endpoint).data[1].get('id')

        client.post(f"{self.endpoint}{first_product_id}/add_to_cart/", {"quantity": 1}, format='json')
        response = client.post(f"{self.endpoint}{second_product_id}/add_to_cart/", {"quantity": 3}, format='json')

        assert response.data.get('cart')[0].get('product_id') == first_product_id
        assert response.data.get('cart')[0].get('quantity') == 1
        assert response.data.get('cart')[1].get('product_id') == second_product_id
        assert response.data.get('cart')[1].get('quantity') == 3
        assert response.data.get('total_amount') == 4

    @pytest.mark.django_db
    def test_patch(self, auto_login_user):
        client, user = auto_login_user()
        product_id_to_change = client.get(self.endpoint).data[0].get('id')
        data_to_update = {
            'name': 'changed name',
            'description': 'changed description',
            'price': 123,
            'in_stock': 321
        }

        user.is_superuser = True
        user.save()
        response = client.patch(self.endpoint + f'{product_id_to_change}/', data_to_update, format='json')
        response_update_data = {
            key: value
            for key, value in response.data.items()
            if key in data_to_update.keys()
        }

        assert response.status_code == 200
        assert response_update_data == data_to_update

    @pytest.mark.django_db
    def test_patch_unauthorized(self, auto_login_user):
        client, user = auto_login_user()
        product_id_to_change = client.get(self.endpoint).data[0].get('id')

        data_to_change = {
            'name': 'changed name',
            'description': 'changed description',
            'price': 123,
            'in_stock': 321
        }
        response = client.patch(self.endpoint + f'{product_id_to_change}/', data_to_change, format='json')

        assert response.status_code == 403
