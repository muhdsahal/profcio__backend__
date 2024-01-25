from django.db import models
from auth_setup.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework.response import Response


# Create your models here.
class EmployeeBooking(models.Model):
    BOOKING_STATUS =(
        ('pending','pending'),
        ('ongoing','ongoing'),
        ('completed','completed'),
    )  
    user = models.ForeignKey(User,on_delete= models.CASCADE,related_name = 'booked_by')
    employee = models.ForeignKey(User,on_delete= models.CASCADE,related_name = 'bookings')
    booking_date = models.DateField()
    price = models.IntegerField(null=True)
    created_date = models.DateField(auto_now=True, null=True)
    is_booked = models.BooleanField(default = False)
    booking_status = models.CharField(max_length = 30,choices=BOOKING_STATUS,default='pending')
    is_review = models.BooleanField(default = True)

    def can_write_review(self):
        if self.booking_status == 'completed':
            days_elasped = (timezone.now().date() - self.booking_date).days
            return days_elasped <= 3 and not self.is_review
        else :
            return False

    def save(self, *args, **kwargs):
        if self.booking_status == 'completed' and self.booking_date > timezone.now().date():
            return Response("Cannot change status to 'completed' for future bookings.")
        
        self.price = self.employee.charge
        super().save(*args, **kwargs)




# review rating model
class Review(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_receiver')
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='review_writer')
    review_text = models.TextField(blank=True, null=True)
    rating = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = ['employee', 'user']



#employee absend model        
class EmployeeAbsence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='absences')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='absentees')
    absence_date = models.DateField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)