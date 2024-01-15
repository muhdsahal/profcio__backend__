from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import BookingSendingMail
from .models import EmployeeBooking

@receiver(post_save,sender=EmployeeBooking)
def send_reciept(sender,instance,created,*args, **kwargs):
    if created:
        username = instance.user.username
        userEmail = instance.user.email
        employeeName = instance.employee.username
        bookedDate = instance.booking_date
        print(username,userEmail,employeeName,bookedDate,'check the signals work or not')
        BookingSendingMail(username,employeeName,bookedDate,userEmail)
        