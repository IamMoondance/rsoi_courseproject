from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    carUid = serializers.UUIDField()
    brand = serializers.CharField()
    car_model = serializers.CharField()
    power = serializers.IntegerField()
    car_type = serializers.CharField()
    price_per_hour = serializers.FloatField()

    def create(self, validated_data):
        return Car.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.carUid = validated_data.get('carUid', instance.carUid)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.car_model = validated_data.get('car_model', instance.car_model)
        instance.power = validated_data.get('power', instance.power)
        instance.car_type = validated_data.get('car_type', instance.car_type)
        instance.price_per_hour = validated_data.get('price_per_hour', instance.price_per_hour)

        instance.save()
        return instance
