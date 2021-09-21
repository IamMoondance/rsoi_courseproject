from django.db import models

## Модель Автомобиль
class Car(models.Model):
    id = models.IntegerField(primary_key=True)
    carUid = models.UUIDField()
    brand = models.CharField(max_length=255)
    car_model = models.CharField(max_length=255)
    power = models.IntegerField()
    car_type = models.CharField(max_length=255)
    price_per_hour = models.FloatField()

    class Meta:
        db_table = 'cars'
