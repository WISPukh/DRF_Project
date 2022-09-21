from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserSerializer


class UsersViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['PUT'])
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
