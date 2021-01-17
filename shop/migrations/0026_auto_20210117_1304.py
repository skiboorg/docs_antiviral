# Generated by Django 3.1.4 on 2021-01-17 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_auto_20210117_1252'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverytype',
            name='price',
            field=models.CharField(max_length=255, null=True, verbose_name='Минимальная стоимость доставки'),
        ),
        migrations.AddField(
            model_name='deliverytype',
            name='time',
            field=models.CharField(max_length=255, null=True, verbose_name='Минимальное время доставки'),
        ),
    ]
