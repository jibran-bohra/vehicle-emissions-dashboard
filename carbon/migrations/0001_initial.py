# Generated by Django 4.2.10 on 2024-03-03 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ToyotaModels',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('vehicle_make', models.CharField(max_length=100)),
            ],
        ),
    ]
