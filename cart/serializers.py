from django.db.models import F
from rest_framework.serializers import ModelSerializer

from .models import Order, OrderItem


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
