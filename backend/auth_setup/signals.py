from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()
from django.dispatch import Signal

# Define a custom signal
user_profile_updated = Signal()

# Connect a receiver function to the custom signal
@receiver(user_profile_updated)
def handle_user_profile_updated(sender, instance, **kwargs):
    
    notification =f"User profile updated: {instance.username}"
    async_to_sync(channel_layer.group_send)(
        'user_group',{
            "type" : "create_notification",
            "message":notification
        }

    )