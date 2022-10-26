from json import dumps

from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer


def generate_json_error_response(status=400, message=''):
    return Response(
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
