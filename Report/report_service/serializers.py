from rest_framework import serializers
from .modeld import OfficeStat, CarStat

class OfficeStatSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    location = serializers.CharField()
    count = serializers.IntegerField()

    def create(self, validated_data):
        return OfficeStat.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.location = validated_data.get('location', instance.location)
        instance.count = validated_data.get('count', instance.count)

        instance.save()
        return instance

class CarStatSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    model = serializers.CharField()
    count = serializers.IntegerField()

    def create(self, validated_data):
        return CarStat.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.model = validated_data.get('model', instance.model)
        instance.count = validated_data.get('count', instance.count)

        instance.save()
        return instance
