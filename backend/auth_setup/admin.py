from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Service)
# admin.site.register(WeeklyAvailability)
admin.site.register(EmployeeBooking)

# admin.site.register(UserDetail)
# admin.site.register(EmployeeDetail)
