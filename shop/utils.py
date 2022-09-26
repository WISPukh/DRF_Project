from json import dumps

from django.http.response import HttpResponse
from rest_framework.serializers import ModelSerializer


def generate_json_error_response(status=400, message=''):
    return HttpResponse(
        dumps({'error': message}),
        content_type='application/json',
        status=status
    )


def get_dynamic_serializer(model=None):
    return type('DynamicSerializer', (ModelSerializer,), {
        'Meta': type('Meta', (), {
            'model': model,
            'fields': '__all__'
        })
    })