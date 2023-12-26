# Generated by Django 4.2.7 on 2023-12-08 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_setup', '0009_service_service_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='Service_image',
            new_name='service_image',
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('all_rounder', 'all_rounder'), ('commercial', 'commercial'), ('home', 'home')], default='home', max_length=20),
        ),
    ]