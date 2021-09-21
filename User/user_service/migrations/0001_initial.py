# Generated by Django 3.1.7 on 2021-08-02 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_uid', models.UUIDField()),
                ('login', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('patronymic', models.CharField(blank=True, default='', max_length=255)),
                ('role', models.BooleanField(default=False)),
                ('refresh_token', models.CharField(max_length=255)),
            ],
        ),
    ]