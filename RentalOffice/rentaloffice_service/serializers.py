from rest_framework import serializers
from .models import RentalOffice, OfficeCar

class RentalOfficeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    officeUid = serializers.UUIDField()
    location = serializers.CharField()

    def create(self, validated_data):
        RentalOffice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.officeUid = validated_data.get('officeUid', instance.officeUid)
        instance.location = validated_data.get('location', instance.location)

        instance.save()
        return instance

class OfficeCarSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    officeUid = serializers.UUIDField()
    carUid = serializers.UUIDField()

    def create(self, validated_data):
        RentalOffice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.officeUid = validated_data.get('officeUid', instance.officeUid)
        instance.carUid = validated_data.get('carUid', instance.carUid)
        
