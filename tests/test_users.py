import re

import pytest
from django.urls import reverse_lazy


class TestUsers:
    endpoint = reverse_lazy('users-list')

    @pytest.mark.django_db
    def test_get_token(self, api_client, django_user_model):
        credentials = dict(email='test@test.test', password='test')
        django_user_model.objects.create_user(**credentials)
        response = api_client.post(reverse_lazy('token_obtain_pair'), credentials, format='json')

        assert response.status_code == 200
        assert isinstance(response.data.get('access'), str)
        assert re.fullmatch(r'(\S+\.\S+\.\S+)', response.data.get('access')) is not None

    @pytest.mark.django_db
    def test_create(self, api_client):
        user = api_client.post(self.endpoint, {'email': 'test@test.test', 'password': '123123qwer'}, format='json')
        assert user.status_code == 201

    @pytest.mark.django_db
    def test_list(self, auto_login_user):
        client, user = auto_login_user()
        response = client.get(self.endpoint)

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_retrieve(self, auto_login_user):
        client, user = auto_login_user()
        response = client.get(f'{self.endpoint}{user.id}/')

        assert response.status_code == 200
        assert response.data.get('id') == user.id

    @pytest.mark.django_db
    def test_retrieve_profile(self, auto_login_user):
        client, user = auto_login_user()
        response = client.get(f'{self.endpoint}{user.id}/profile/')

        assert response.status_code == 200
        assert response.data.get('id') == user.id

    @pytest.mark.django_db
    def test_patch_profile(self, auto_login_user):
        client, user = auto_login_user()
        update_data = {
            'bio': 'amazing hacker',
            'age': 9,
            'phone': 88005553535
        }

        response = client.patch(f'{self.endpoint}{user.id}/profile/', update_data, format='json')
        response_update_data = {
            key: value
            for key, value in response.data.items()
            if key in update_data.keys()
        }

        assert response.status_code == 200
        assert response.data.get('id') == user.id
        assert response_update_data == update_data
