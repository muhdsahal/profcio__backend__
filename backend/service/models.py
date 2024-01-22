from django.db import models

# Create your models here.
class ServiceCategory(models.Model):
    name = models.CharField(max_length=50,unique = True)

    # def __str__(self):
    #     return super().self.name
    
class Service(models.Model):
   
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(ServiceCategory,on_delete=models.CASCADE)
    service_image =  models.ImageField(upload_to='service',blank=True,null=True)
    is_available = models.BooleanField(default=False)
    
    # def __str__(self):
    #     return super().self.name