from django.db import models

# Create your models here
from auth_setup.models import User
class Message(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name='sent_messages')
    reciever=models.ForeignKey(User,on_delete=models.CASCADE,related_name='recieved_messages')
    message =models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=200)
    timestamp=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
            return f"{self.sender.username} sent to {self.reciever.username} at {self.timestamp}"