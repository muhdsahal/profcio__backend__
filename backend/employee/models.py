from django.db import models
from auth_setup.models import User

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
    def save(self,*args, **kwargs):
        self.price = self.employee.charge
        super().save(*args, **kwargs)