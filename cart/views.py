from django.contrib import messages
from django.db.transaction import atomic
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from users.mixins import CheckUserIsOwnerMixin
from .services import CartActionsService
from .models import OrderItem, Order
from .tasks import order_created
from .serializers import OrderSerializer


class OrderHistoryViewSet(CheckUserIsOwnerMixin, ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        self.queryset = Order.objects.filter(customer_id=self.request.user.pk, status__in=[
            'CREATED',
            'PAID',
            'IS_DELIVERING',
            'DELIVERED'
        ])
        return self.queryset


class CartViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(customer_id=self.request.user.pk, status='CART')

    @atomic
    def partial_update(self, request, *args, **kwargs):
        cart_actions_service = CartActionsService
        order = cart_actions_service.change_products_in_cart(self, request)  # noqa
        return Response(OrderSerializer(order).data)
