# Generated by Django 5.1.1 on 2024-09-12 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0003_reservation_numero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='numero',
        ),
    ]
