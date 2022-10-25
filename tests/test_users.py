import re

import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK


class TestUsers:
    @pytest.mark.django_db
    def test_get_token(self, api_client, django_user_model):
        credentials = dict(email='test@test.test', password='test')
        django_user_model.objects.create_user(**credentials)
        response = api_client.post('/api/token/', credentials, format='json')

        assert response.status_code == HTTP_200_OK
        assert isinstance(response.data.get('access'), str)
        assert re.fullmatch(r'(\S+\.\S+\.\S+)', response.data.get('access')) is not None

    @pytest.mark.django_db
    def test_create(self, api_client):
        user = api_client.post('/api/users/', {'email': 'test@test.test', 'password': '123123qwer'}, format='json')
        assert user.status_code == 201

    @pytest.mark.django_db
    def test_list(self, auto_login_user):
        client, user = auto_login_user()
        response = client.get('/api/users/')

        assert response.status_code == HTTP_200_OK

    @pytest.mark.django_db
    def test_retrieve(self, auto_login_user):
        client, user = auto_login_user()
        response = client.get(reverse('users-detail', args=[user.id]))

        assert response.status_code == HTTP_200_OK
        assert response.data.get('id') == user.id

    @pytest.mark.django_db
    def test_retrieve_profile(self, auto_login_user):
        client, user = auto_login_user()
        url = reverse('profile', args=[user.id])
        response = client.get(url, follow=True)

        assert response.status_code == HTTP_200_OK
        assert response.data.get('id') == user.id

    @pytest.mark.django_db
    def test_patch_profile(self, auto_login_user):
        client, user = auto_login_user()
        url = reverse('profile', args=[user.id])
        update_data = {
            'bio': 'amazing hacker',
            'age': 9,
            'phone': 88005553535
        }
        response = client.patch(url, data=update_data, format='json')
        response_update_data = {
            key: value
            for key, value in response.data.items()
            if key in update_data.keys()
        }

        assert response.status_code == HTTP_200_OK
        assert response.data.get('id') == user.id
        assert response_update_data == update_data
