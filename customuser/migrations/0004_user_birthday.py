# Generated by Django 3.1.4 on 2021-01-12 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0003_auto_20201216_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='Д/Р'),
        ),
    ]