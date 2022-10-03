from rest_framework.viewsets import ModelViewSet

from shop.utils import generate_json_error_response
from .models import Profile
from .serializers import ProfileSerializer


class ProfileDetailViewSet(ModelViewSet):
    model = Profile
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.kwargs.get('pk'))

    def patch(self, request, *args, **kwargs):
        # only superuser can change other users' profiles
        if request.user.pk != kwargs.get('pk') and request.user.is_superuser:
            return self.update(request, *args, **kwargs)
        if request.user.pk == kwargs.get('pk'):
            return self.update(request, *args, **kwargs)
        return generate_json_error_response(status=403, message="You can not change other user's profile info")
