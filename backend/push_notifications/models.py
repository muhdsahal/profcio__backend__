from django.db import models


# Create your models here.
class Notifications(models.Model):
    NOTIFCATION_TYPES = (
        ('user', 'user'),
        ('admin', 'admin'),
        ('employee', 'employee')
    )
    notification_text = models.TextField()
    notificatio_type = models.CharField(max_length = 30, choices = NOTIFCATION_TYPES, default = 'user')
    