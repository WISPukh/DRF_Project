from django.urls import path, include
from .views import ProfileDetailViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('', ProfileDetailViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}))
]
