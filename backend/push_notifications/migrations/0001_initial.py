# Generated by Django 4.2.7 on 2024-01-31 07:05

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Notifications",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("notification_text", models.TextField()),
                (
                    "notificatio_type",
                    models.CharField(
                        choices=[
                            ("user", "user"),
                            ("admin", "admin"),
                            ("employee", "employee"),
                        ],
                        default="user",
                        max_length=30,
                    ),
                ),
            ],
        ),
    ]