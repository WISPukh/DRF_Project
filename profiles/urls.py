from django.urls import path, include
from .views import ProfileDetailViewSet
from rest_framework.routers import SimpleRouter


router = SimpleRouter()
router.register('', ProfileDetailViewSet, basename='profile_detail')

urlpatterns = [
    path('', include(router.urls))
]
