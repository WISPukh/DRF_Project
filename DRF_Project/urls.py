from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from cart.urls import cart, orders

schema_view = get_schema_view(
   openapi.Info(
      title="KitchenAid API",
      default_version='v1',
      description="YEAH GOD DAMN THAT **** WORKS",
      terms_of_service="https://swagger.io/terms/",
      contact=openapi.Contact(email="puhoff.ol@yandex.ru"),
      license=openapi.License(name="MY DAMN LICENSE"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # noqa
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # noqa
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # noqa

    path('admin/', admin.site.urls),
    # authorization via token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/users/', include('users.urls')),
    path('api/products/', include('shop.urls')),
    path('api/orders/history/', include(orders.urls)),
    path('api/cart/', include(cart.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL)