from django.contrib import admin
from .models import Service,ServiceCategory
# Register your models here.
admin.site.register(ServiceCategory)
admin.site.register(Service)