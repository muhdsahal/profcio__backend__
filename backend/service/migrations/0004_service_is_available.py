# Generated by Django 4.2.7 on 2024-01-18 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
    ]
