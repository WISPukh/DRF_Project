from django.urls import path
from .views import ProfileDetailViewSet

urlpatterns = [
    path('', ProfileDetailViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}))
]
