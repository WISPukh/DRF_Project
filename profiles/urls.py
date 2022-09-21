from django.urls import path, include
from .views import ProfileDetailViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', ProfileDetailViewSet, basename='profile_detail')

urlpatterns = [
    path('', include(router.urls))
]
