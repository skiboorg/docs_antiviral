# Generated by Django 3.1.4 on 2021-01-11 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='name_lower',
            field=models.CharField(editable=False, max_length=255, null=True, verbose_name='Название города'),
        ),
    ]
