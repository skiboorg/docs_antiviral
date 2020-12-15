# Generated by Django 3.1.4 on 2020-12-14 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20201214_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemtype',
            name='collection',
        ),
        migrations.AddField(
            model_name='item',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='shop.collection', verbose_name='Коллекция'),
        ),
    ]
