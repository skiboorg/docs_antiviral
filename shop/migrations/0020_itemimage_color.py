# Generated by Django 3.1.4 on 2021-01-07 17:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_auto_20201229_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemimage',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.itemcolor', verbose_name='Цвет'),
        ),
    ]
