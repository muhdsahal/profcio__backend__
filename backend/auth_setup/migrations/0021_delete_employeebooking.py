# Generated by Django 4.2.7 on 2024-01-10 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_setup', '0020_delete_service_delete_servicecategory'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmployeeBooking',
        ),
    ]
