from celery import shared_task 
from django.core.mail import send_mail
from .models import EmployeeBooking
from datetime import timedelta
from django.utils import timezone
import logging
from datetime import datetime, timedelta, time



@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Done"

@shared_task
def BookingSendingMail(username,employeeName,bookedDate,userEmail):
    subject ="Profcio | Booking confirmation"
        
    message = f"""Hy {username}. Your Booking has been successfully.
    Your selected employee: {employeeName} in {bookedDate} day.
    Thank you for choosing Profcio ."""
    from_email = "profcioweb@gmail.com"
    recipient_list = [userEmail] 
    send_mail(subject,message, from_email, recipient_list, fail_silently=True)


@shared_task
def send_booking_reminders():
    try:
        # Calculate the target time (8:40 PM) on the previous day
        # target_time = datetime.combine(time(20, 40), time.min)
        current_time = timezone.now()

        # If the current time is before the target time, use the previous day
        if current_time.time() < target_time.time():
            target_time -= timedelta(days=1)

        # Calculate the time 8 hours before the target time
        # eight_hours_before_target = target_time - timedelta(hours=8)

        # Filter bookings within the time range
        bookings_to_remind = EmployeeBooking.objects.filter(
            booking_date__lt=target_time,
            is_booked=True,
        )

        for booking in bookings_to_remind:
            subject = 'Profcio || Booking Reminder'
            message = f"Your booking with {booking.employee.username} is scheduled \n for {booking.booking_date}. "
            from_email = 'profcioweb@gmail.com'
            to_email = [booking.user.email]

            send_mail(subject, message, from_email, to_email)

        logging.info('Booking reminders sent successfully.')
    except Exception as e:
        logging.error(f'Error sending booking reminders: {e}')




# @shared_task
# def celerybeatcheck():
#     print("beat working.................")
#     subject = "Profcio | Booking confirmation"
        
#     message = f"""Hy Your Booking has been successfully.
#     Your selected employee:  in day.
#     Thank you for choosing Profcio ."""
    
#     from_email = "profcioweb@gmail.com"
#     recipient_list = ['sahalshalu830@gmail.com']  # Use a list or tuple for recipient_list

#     send_mail(subject, message, from_email, recipient_list, fail_silently=True)

# @shared_task