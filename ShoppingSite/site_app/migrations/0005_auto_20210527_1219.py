# Generated by Django 3.1.4 on 2021-05-27 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_app', '0004_auto_20210526_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='subtotal',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
