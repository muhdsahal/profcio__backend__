# Generated by Django 4.2.7 on 2023-11-28 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_setup', '0005_remove_userdetail_user_user_charge_user_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=100)),
            ],
        ),
    ]
