import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .factories import (
    FridgeFactory,
    TeapotFactory,
    CombineFactory,
    BlenderFactory,
    PanelFactory,
    MixerFactory,
    ContentType
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auto_login_user(db, api_client):
    def make_auto_login():
        user = User.objects.get(email='test@chel.com')
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return api_client, user

    return make_auto_login


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):  # noqa
    with django_db_blocker.unblock():
        type_factories_mapping = {
            'mixer': MixerFactory,
            'blender': BlenderFactory,
            'combine': CombineFactory,
            'fridge': FridgeFactory,
            'panel': PanelFactory,
            'teapot': TeapotFactory
        }

        for product_type, product_factory in type_factories_mapping.items():
            product_factory.create(content_type=ContentType.objects.get(model=product_type))

        User.objects.create_user(email='test@chel.com', password='test_password')
