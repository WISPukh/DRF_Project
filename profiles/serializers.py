from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Profile


class ProfileSerializer(serializers.Serializer): # noqa
    id = serializers.IntegerField(read_only=True)
    bio = serializers.CharField(required=False)
    birthday = serializers.DateField(required=False)
    phone = serializers.IntegerField(required=False)
    age = serializers.IntegerField(required=False)
    region = serializers.CharField(required=False)
    user_id = serializers.IntegerField(read_only=True)

    default_validators = [UniqueValidator(Profile.objects.all())]

    def update(self, instance, validated_data):
        instance.bio = validated_data.get('bio', instance.bio)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.age = validated_data.get('age', instance.age)
        instance.region = validated_data.get('region', instance.region)
        instance.save()
        return instance
