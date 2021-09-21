from rest_framework import serializers

from .models import Payment

class PaymentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    rent_uid = serializers.UUIDField()
    status = serializers.CharField()
    price = serializers.FloatField()

    def create(self, validated_data):
        return Payment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.rent_uid = validated_data.get('rent_uid', instance.rent_uid)
        instance.status = validated_data.get('status', instance.status)
        instance.price = validated_data.get('price', instance.price)

        instance.save()
        return instance
