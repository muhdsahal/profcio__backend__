from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

timezone.now()

# Create your models here.

class User(AbstractUser):
    USER_TYPES = (
        ('user', 'user'),
        ('employee', 'employee'),
        ('admin', 'admin'),
    )

    username =models.CharField(max_length=250,null=True)
    email = models.EmailField(max_length=250,unique=True)
    password = models.CharField(max_length=250)
    profile_photo = models.ImageField(upload_to='profile',blank=True,null=True)
    is_active = models.BooleanField(default=False)
    user_type = models.CharField(max_length=20,choices=USER_TYPES,default='user')
    is_google = models.BooleanField(default=False)
    phone_number = PhoneNumberField(blank=True)
    work = models.CharField(max_length=100,blank=True)
    place = models.CharField(max_length=150, default="Unknown",blank=True,null=True)
    description = models.TextField(null=True,blank=True)
    experience = models.IntegerField(blank=True,null=True)
    charge = models.IntegerField(blank=True,null=True)
    
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

class ServiceCategory(models.Model):
    name = models.CharField(max_length=50,unique = True)
    
    def __str__(self):
        return self.name


class Service(models.Model):
   
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ServiceCategory,on_delete=models.CASCADE)
    service_image =  models.ImageField(upload_to='profile',blank=True,null=True)


class EmployeeBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_by')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    price = models.IntegerField(null=True)
    created_date = models.DateField(auto_now=True, null=True)
    is_booked = models.BooleanField(default = False)

    


# WEEKDAYS_CHOICES = (
#     (1, 'Monday'),
#     (2, 'Tuesday'),
#     (3, 'Wednesday'),
#     (4, 'Thursday'),
#     (5, 'Friday'),
#     (6, 'Saturday'),
#     (7, 'Sunday'),
# )

# class WeeklyAvailability(models.Model):
#     employee = models.ForeignKey(User, on_delete=models.CASCADE)
#     day_of_week = models.IntegerField(choices=WEEKDAYS_CHOICES)
#     is_available = models.BooleanField()

# class EmployeeBooking(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_by')
#     employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
#     booking_date = models.DateField()
#     created_date = models.DateField(auto_now=True, null=True)