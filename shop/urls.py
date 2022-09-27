from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import ProductViewSet, AddToCartViewSet


router = SimpleRouter()
router.register('', ProductViewSet, basename='products')

make_order = SimpleRouter()
make_order.register('', AddToCartViewSet, basename='add_to_cart')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/order/', include(make_order.urls))
]
