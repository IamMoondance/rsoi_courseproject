from django.db import models

## Модель Пользователь
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    user_uid = models.UUIDField()
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, default='', blank=True)
    role = models.BooleanField(default=False)
    refresh_token = models.CharField(max_length=255)

    class Meta:
        db_table = 'users'