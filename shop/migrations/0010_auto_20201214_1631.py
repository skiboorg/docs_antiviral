# Generated by Django 3.1.4 on 2020-12-14 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20201214_1435'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='discount_description',
        ),
        migrations.RemoveField(
            model_name='item',
            name='short',
        ),
        migrations.AddField(
            model_name='item',
            name='discount',
            field=models.IntegerField(default=0, verbose_name='Скидка'),
        ),
        migrations.AddField(
            model_name='item',
            name='short_description',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Короткое описание'),
        ),
    ]
