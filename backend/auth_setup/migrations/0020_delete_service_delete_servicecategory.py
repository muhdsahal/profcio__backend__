# Generated by Django 4.2.7 on 2024-01-05 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_setup', '0019_employeebooking_is_booked_employeebooking_price_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Service',
        ),
        migrations.DeleteModel(
            name='ServiceCategory',
        ),
    ]
