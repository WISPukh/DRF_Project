from rest_framework.viewsets import ModelViewSet

from shop.utils import generate_json_error_response
from .models import User
from .serializers import UserSerializer


class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    http_method_names = ['get', 'patch', 'post']

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return User.objects.filter(pk=self.request.user.pk)
        return User.objects.all()

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return generate_json_error_response(403, 'You can not change anything')
        return self.update(request, *args, **kwargs)
