from django.db import models

class OfficeStat(models.Model):
    id = models.IntegerField(primary_key=True)
    location = models.CharField(max_length=255)
    count = models.IntegerField()

    class Meta:
        db_table = 'officestat'

class CarStat(models.Model):
    id = models.IntegerField(primary_key=True)
    model = models.CharField(max_length=255)
    count = models.IntegerField()

    class Meta:
        db_table = 'carstat'
