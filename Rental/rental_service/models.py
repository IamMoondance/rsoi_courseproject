from django.db import models

## Модель Аренда
class Rental(models.Model):
    id = models.UUIDField(primary_key=True)
    car_uid = models.UUIDField()
    user_uid = models.UUIDField()
    payment_uid = models.UUIDField()
    rent_from = models.DateTimeField()
    rent_until = models.DateTimeField()
    status = models.CharField(max_length=255)
    rec_office_uid = models.UUIDField()
    ret_office_uid = models.UUIDField()

    class Meta:
        db_table = 'rentals'
