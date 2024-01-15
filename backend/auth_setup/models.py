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


class Notifications(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)

    def __str__(self):

        return self.text

