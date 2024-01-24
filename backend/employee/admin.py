from django.contrib import admin
from .models import EmployeeBooking,Review,EmployeeAbsence
# Register your models here.
admin.site.register(EmployeeBooking)
admin.site.register(EmployeeAbsence)
admin.site.register(Review)