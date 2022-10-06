from django.urls import path, include
from rest_framework.routers import SimpleRouter

from profiles.views import ProfileDetailViewSet
from .views import UsersViewSet


router = SimpleRouter()
router.register(r'', UsersViewSet, basename='users')
router.register(r'', ProfileDetailViewSet, basename='profile_detail')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/profile/', include('profiles.urls')),
]
