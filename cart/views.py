from django.http.response import HttpResponse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from users.mixins import CheckUserIsOwnerMixin
from .models import Order
from .serializers import CartSerializer, OrderSerializer
from .services import CartActionsService


class OrderHistoryViewSet(CheckUserIsOwnerMixin, ModelViewSet):
    serializer_class = OrderSerializer
    http_method_names = ("GET",)

    def get_queryset(self):
        self.queryset = Order.objects.filter(customer_id=self.request.user.pk, status__in=[
            'CREATED',
            'PAID',
            'IS_DELIVERING',
            'DELIVERED'
        ])
        return self.queryset


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.request.user.pk, status='CART')

    def post(self, request, *args, **kwargs):
        """
        desc: creates an order from existing products in cart
        :param request:
        :param args:
        :param kwargs:
        :return: json: with your order
        """
        service = self.get_service()
        order = service.make_order()
        if isinstance(order, HttpResponse):
            return order
        return Response(CartSerializer(order).data)

    def partial_update(self, request, *args, **kwargs):
        service = self.get_service()
        order = service.change_products_in_cart()
        return Response(CartSerializer(order).data)

    def get_service(self):
        return CartActionsService(user=self.request.user, request_data=self.request.data, order=self.get_object())
