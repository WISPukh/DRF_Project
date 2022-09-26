from django.contrib.contenttypes.models import ContentType
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Product
from .serializers import ProductSerializer
from .utils import generate_json_error_response, get_dynamic_serializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        self.queryset = Product.objects.all().order_by('pk')
        return self.queryset

    def list(self, request, *args, **kwargs):
        if category := request.query_params.get('category'):
            if not ContentType.objects.filter(model=category).exists():
                return generate_json_error_response(HTTP_400_BAD_REQUEST, 'Incorrect category')
            content = ContentType.objects.get(model=category).model_class().objects.all()
            return Response(self.serializer_class(content, many=True).data)
        return Response(self.serializer_class(self.queryset, many=True).data)

    def retrieve(self, request, *args, **kwargs):
        dynamic_model = ContentType.objects.get(pk=self.get_object().content_type_id).model_class()
        dynamic_serializer = get_dynamic_serializer(dynamic_model)
        instance = dynamic_model.objects.get(pk=kwargs.get('pk'))
        return Response(dynamic_serializer(instance).data)

    def create(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return generate_json_error_response(HTTP_403_FORBIDDEN, 'You have no access to this functionality')

        model = ContentType.objects.get(pk=request.data.get('content_type')).model_class()
        dynamic_serializer = get_dynamic_serializer(model)

        serializer = dynamic_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def partial_update(self, request, *args, **kwargs):
        model = ContentType.objects.get(pk=self.get_object().content_type_id).model_class()
        dynamic_serializer = get_dynamic_serializer(model)

        instance = model.objects.get(pk=kwargs.get('pk'))
        serializer = dynamic_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
