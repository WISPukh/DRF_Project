from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderHistoryViewSet, CartViewSet

orders = DefaultRouter()
orders.register('', OrderHistoryViewSet, basename='orders')

cart = DefaultRouter()
cart.register('', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(orders.urls)),
]
