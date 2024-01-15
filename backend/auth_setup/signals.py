from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save,sender=User)
def send_reciept(sender,instance,created,*args, **kwargs):
    if created:
        notification_text = f"your booking success fully complated"
