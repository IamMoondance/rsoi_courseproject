from django.db import models

## Модель Офис аренды
class RentalOffice(models.Model):
    id = models.IntegerField(primary_key=True)
    officeUid = models.UUIDField()
    location = models.CharField(max_length=255)

    class Meta:
        db_table = 'rentaloffices'
    

## Модель связи автомобиля с офисом
class OfficeCar(models.Model):
    id = models.UUIDField(primary_key=True)
    officeUid = models.UUIDField()
    carUid = models.UUIDField()

    class Meta:
        db_table = 'officecars'
