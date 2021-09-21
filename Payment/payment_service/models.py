from django.db import models

## Модель Оплата
class Payment(models.Model):
    id = models.IntegerField(primary_key=True)
    rent_uid = models.UUIDField()
    status = models.CharField(max_length=16)
    price = models.FloatField()

    class Meta:
        db_table = 'payments'
