from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer


class ProfileDetailViewSet(ModelViewSet):
    model = Profile
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.kwargs.get('pk'))

    def put(self, request, *args, **kwargs):
        # only superuser can change other users' profiles
        if request.user.pk != kwargs.get('pk') and request.user.is_superuser:
            return Response(status=HTTP_403_FORBIDDEN, data="You can not change other user's profile info")
        return self.update(request, *args, **kwargs)
