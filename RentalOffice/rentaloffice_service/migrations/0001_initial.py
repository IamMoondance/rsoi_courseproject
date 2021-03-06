# Generated by Django 3.1.7 on 2021-09-12 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OfficeCar',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('officeUid', models.UUIDField()),
                ('carUid', models.UUIDField()),
            ],
            options={
                'db_table': 'officecars',
            },
        ),
        migrations.CreateModel(
            name='RentalOffice',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('officeUid', models.UUIDField()),
                ('location', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'rentaloffices',
            },
        ),
    ]
