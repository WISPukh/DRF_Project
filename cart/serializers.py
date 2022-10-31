from rest_framework.serializers import ModelSerializer, IntegerField

from .models import Order, OrderItem


class CartItemsSerializer(ModelSerializer):
    product_id = IntegerField(source='product_id_id')

    class Meta:
        model = OrderItem
        fields = ('product_id', 'quantity',)


class CartSerializer(ModelSerializer):
    cart = CartItemsSerializer(many=True, source='product', required=False)
    total_price = IntegerField(source='calculated_total_price', required=False)
    total_amount = IntegerField(source='calculated_total_amount', required=False)

    class Meta:
        model = Order
        fields = ('id', 'cart', 'total_price', 'total_amount', 'city', 'address', 'customer_id',)


class OrderItemsSerializer(ModelSerializer):
    product_id = IntegerField(source='product_id_id')

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    product = OrderItemsSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
