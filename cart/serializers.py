from rest_framework.serializers import ModelSerializer, IntegerField

from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):
    product_id = IntegerField(source='product_id_id')

    class Meta:
        model = OrderItem
        fields = ('product_id', 'quantity', )


class OrderSerializer(ModelSerializer):
    cart = OrderItemSerializer(many=True, source='product')

    class Meta:
        model = Order
        fields = ('id', 'cart', 'total_price', 'total_amount', 'city', 'address', 'customer_id',)
