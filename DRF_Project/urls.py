from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from cart.urls import cart, orders

urlpatterns = [
    path('admin/', admin.site.urls),
    # authorization via token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/users/', include('users.urls')),
    path('api/products/', include('shop.urls')),
    path('api/orders/history/', include(orders.urls)),
    path('api/cart/', include(cart.urls))
]
