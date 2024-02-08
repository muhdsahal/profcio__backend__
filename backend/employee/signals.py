from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from .tasks import BookingSendingMail,BookingMailForEmployee
from .models import EmployeeBooking
from push_notifications.models import Notifications
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.dispatch import Signal

booking_notification = Signal()
channel_layer = get_channel_layer()


@receiver(post_save,sender=EmployeeBooking)
def send_reciept(sender,instance,created,*args, **kwargs):
    if created:
        username = instance.user.username
        userEmail = instance.user.email
        employeeName = instance.employee.username
        bookedDate = instance.booking_date
        price = instance.price
        # message = 
        BookingSendingMail(username,employeeName,bookedDate,userEmail, price)


@receiver(post_save,sender=EmployeeBooking)
def send_reciept_employee(sender,instance,created,*args, **kwargs):
    if created:
        username = instance.user.username
        employeeEmail = instance.employee.email
        employeeName = instance.employee.username
        BookedDate = instance.booking_date

        BookingMailForEmployee(username,employeeName,employeeEmail, BookedDate)


@receiver(booking_notification)
def send_booking_notification(sender,instance, **kwargs):
        notification_text = f'you booking for {instance.employee.username} is completed successfully'
        print(notification_text,"------------------->>>>>")
        
        async_to_sync(channel_layer.group_send)(
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