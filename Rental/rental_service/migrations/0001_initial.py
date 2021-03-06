# Generated by Django 3.2.7 on 2021-09-04 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('car_uid', models.UUIDField()),
                ('user_uid', models.UUIDField()),
                ('payment_uid', models.UUIDField()),
                ('rent_from', models.DateTimeField()),
                ('rent_until', models.DateTimeField()),
                ('status', models.CharField(max_length=255)),
                ('rec_office_uid', models.UUIDField()),
                ('ret_office_uid', models.UUIDField()),
            ],
        ),
    ]
