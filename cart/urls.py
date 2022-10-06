from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import OrderHistoryViewSet, CartViewSet

orders = SimpleRouter()
orders.register('', OrderHistoryViewSet, basename='orders')

cart = SimpleRouter()
cart.register('', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(orders.urls)),
]
