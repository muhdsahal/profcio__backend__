# Generated by Django 4.2.7 on 2023-12-24 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_setup', '0016_userbookedday'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField()),
                ('created_date', models.DateField(auto_now=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='employeeavailability',
            name='available_days',
        ),
        migrations.RemoveField(
            model_name='employeeavailability',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='userbookedday',
            name='booked_day',
        ),
        migrations.RemoveField(
            model_name='userbookedday',
            name='employee',
        ),
        migrations.RemoveField(
            model_name='userbookedday',
            name='user',
        ),
        migrations.DeleteModel(
            name='AvailableDay',
        ),
        migrations.DeleteModel(
            name='EmployeeAvailability',
        ),
        migrations.DeleteModel(
            name='UserBookedDay',
        ),
    ]
