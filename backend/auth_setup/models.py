from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
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

    profile_photo = models.ImageField(upload_to='images/profile',blank=True,null=True)

    is_active = models.BooleanField(default=False)

    user_type = models.CharField(max_length=20,choices=USER_TYPES,default='user')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    # def save(self,*args,**kwargs):
    #     created = not self.pk # Check if this is a new instance being created
    #     super(User,self).save(*args,**kwargs)

    #     if created and self.user_type == 'employee':
    #         #create a notification when new employee is created
    #         notification = AdminNotificationCreate(
    #             name =f"Name User Created :{self.email}",
    #             description = f"A New Employee created named '{self.name}'",
    #             is_opened = False,
    #             notification_type = 'register',
    #         )
    #         notification.save()

class EmployeeDetail(models.Model):

    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    contact = models.CharField(max_length=50)

    description = models.TextField(null=True)

class UserDetail(models.Model):

    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    occupation = models.CharField(max_length=50)

    contact = models.CharField(max_length=50)
