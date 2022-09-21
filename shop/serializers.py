from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=250)
    price = serializers.IntegerField()
    in_stock = serializers.IntegerField()
    # category = serializers.ManyToManyField('Category')
    img = serializers.CharField()
    # content_type = serializers.ForeignKey(ContentType, on_delete=models.CASCADE, default=50)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.in_stock = validated_data.get('in_stock', instance.in_stock)
        instance.img = validated_data.get('img', instance.img)
        return instance
