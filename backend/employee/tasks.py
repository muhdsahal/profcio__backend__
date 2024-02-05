from celery import shared_task 
from django.core.mail import send_mail
from .models import EmployeeBooking
from datetime import timedelta
from django.utils import timezone
import logging
from datetime import datetime, timedelta, time
from django.template.loader import render_to_string


@shared_task(bind=True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Done"

# @shared_task
# def BookingSendingMail(username,employeeName,bookedDate,userEmail, price):
#     subject ="Profcio | Booking confirmation"
        
#     message = f"""Hy {username}. Your Booking has been successfully.
#     Your selected employee: {employeeName} in {bookedDate} day.
#     Thank you for choosing Profcio ."""
#     from_email = "profcioweb@gmail.com"
#     recipient_list = [userEmail] 
#     send_mail(subject,message, from_email, recipient_list, fail_silently=True)

@shared_task
def BookingSendingMail(username, employeeName, bookedDate, userEmail, price):
    subject = "Profcio | Booking Confirmation And Invoice"

    # Render HTML template
    html_content = render_to_string('invoice_template1.html', {'instance': 
                                    {'user': {'username': username}, 
                                    'employee': {'username': employeeName},
                                    'booking_date': bookedDate, 'price': price}})

    from_email = "profcioweb@gmail.com"
    recipient_list = [userEmail]
    
    # Send email with HTML content
    send_mail(subject, "", from_email, recipient_list, html_message=html_content, fail_silently=True)

@shared_task
def send_booking_reminders():
    try:
        # Calculate the target time (10:00 AM) for the current day
        target_time = datetime.combine(time(11, 0), time.min)
        current_time = timezone.now()

        # Filter bookings within the time range for the current day
        bookings_to_remind = EmployeeBooking.objects.filter(
            booking_date__gte=current_time,
            booking_date__lt=target_time + timedelta(days=1),  
            is_booked=True,
        )

        print(bookings_to_remind, 'bookings_to_remindbookings_to_remindbookings_to_remind')
        
        for booking in bookings_to_remind:
            subject = 'Profcio || Booking Reminder'
            message = f"Your booking with {booking.employee.username} is scheduled for {booking.booking_date}."
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
#     recipient_list = ['sahalshalu830@gmail.com']  

#     send_mail(subject, message, from_email, recipient_list, fail_silently=True)

# @shared_task