from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from .tasks import BookingSendingMail
from .models import EmployeeBooking

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()


@receiver(post_save,sender=EmployeeBooking)
def send_reciept(sender,instance,created,*args, **kwargs):
    if created:
        username = instance.user.username
        userEmail = instance.user.email
        employeeName = instance.employee.username
        bookedDate = instance.booking_date
        BookingSendingMail(username,employeeName,bookedDate,userEmail)
   
@receiver(post_save, sender=EmployeeBooking)
def send_booking_notification(created, instance, sender, *args, **kwargs):
    if created:
        notification_text = f'you booking for {instance.employee.username} is completed successfully'
        print(notification_text,"------------------->>>>>")
        async_to_sync = (channel_layer.group_send)(
            "user_group",{
                "type":"create_notification",
                "message":notification_text,

            }
        )

# @receiver(post_save,sender=EmployeeBooking)
# def schedule_booking_reminder(sender,instance,created,**kwargs):
#     if created:
#          # Schedule the task to run 8 hours before booking_date
#         send_booking_reminder.apply_async((instance.id,),eta=instance.booking_date - timedelta(hours=8))