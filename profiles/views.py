from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Profile
from .serializers import ProfileSerializer


class ProfileDetailViewSet(ModelViewSet):
    model = Profile
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.kwargs.get('pk'))

    @action(detail=True, methods=['put'])
    def put(self, request, *args, **kwargs):
        profile = self.model.objects.get(user_id=self.kwargs.get('pk'))
        return self.update(request, *args, **kwargs)
