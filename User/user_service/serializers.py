from rest_framework import serializers
from .models import User

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_uid = serializers.UUIDField()
    login = serializers.CharField()
    password = serializers.CharField()
    surname = serializers.CharField()
    name = serializers.CharField()
    patronymic = serializers.CharField(allow_blank=True)
    role = serializers.BooleanField()
    refresh_token = serializers.CharField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.user_uid = validated_data.get('user_uid', instance.user_uid)
        instance.login = validated_data.get('login', instance.login)
        instance.password = validated_data.get('password', instance.password)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.name = validated_data.get('name', instance.name)
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)
        instance.role = validated_data.get('role', instance.role)
        instance.refresh_token = validated_data.get('refresh_token', instance.refresh_token)

        instance.save()
        return instance
