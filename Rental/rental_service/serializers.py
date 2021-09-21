from rest_framework import serializers

from .models import Rental


##TODO обновить
class RentalSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    car_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    payment_id = serializers.IntegerField()
    rent_from = serializers.DateTimeField()
    rent_until = serializers.DateTimeField()
    status = serializers.CharField()
    rec_location = serializers.CharField()
    ret_location = serializers.CharField()
    rec_office_id = serializers.IntegerField()
    ret_office_id = serializers.IntegerField()

    def create(self, validated_data):
        return Rental.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.car_id = validated_data.get('car_id', instance.car_id)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.payment_id = validated_data.get('payment_id', instance.payment_id)
        instance.rent_from = validated_data.get('rent_from', instance.rent_from)
        instance.rent_until = validated_data.get('rent_until', instance.rent_until)
        instance.status = validated_data.get('status', instance.status)
        instance.rec_location = validated_data.get('rec_location', instance.rec_location)
        instance.ret_location = validated_data.get('ret_location', instance.ret_location)
        instance.rec_office_id = validated_data.get('rec_office_id', instance.rec_office_id)
        instance.ret_office_id = validated_data.get('ret_office_id', instance.ret_office_id)

        instance.save()
        return instance

