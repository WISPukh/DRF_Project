from random import randint

import factory
from django.contrib.contenttypes.models import ContentType

from shop.models import (
    Product,
    Mixer,
    Blender,
    Teapot,
    Combine,
    Panel,
    Fridge
)


def get_price():
    return randint(499, 9999)


def get_in_stock():
    return randint(1, 100)


class BaseProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        abstract = True

    name = factory.Faker('sentence', nb_words=2)
    description = factory.Faker('text')
    price = factory.Sequence(lambda _: get_price())
    in_stock = factory.Sequence(lambda _: get_in_stock())
    img = factory.Faker('sentence', nb_words=2)
    content_type = factory.Iterator(ContentType.objects.all())


class MixerFactory(BaseProductFactory):
    class Meta:
        model = Mixer


class BlenderFactory(BaseProductFactory):
    class Meta:
        model = Blender


class FridgeFactory(BaseProductFactory):
    class Meta:
        model = Fridge


class TeapotFactory(BaseProductFactory):
    class Meta:
        model = Teapot


class PanelFactory(BaseProductFactory):
    class Meta:
        model = Panel


class CombineFactory(BaseProductFactory):
    class Meta:
        model = Combine
