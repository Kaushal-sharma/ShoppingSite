# Generated by Django 3.1.4 on 2021-05-27 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_app', '0005_auto_20210527_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='subtotal',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='total',
        ),
    ]