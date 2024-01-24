from celery import shared_task 
from django.core.mail import send_mail
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
def celerybeatcheck():
    print("beat working.................")