from auth_setup.models import User
from rest_framework import serializers
from .models import EmployeeBooking,EmployeeAbsence


class CustomUserserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email","phone_number"]
    
class EmployeeBookingSerializer(serializers.ModelSerializer):
    userDetails = CustomUserserializer(source = 'user', read_only = True)
    employeeDetails = CustomUserserializer(source = 'employee', read_only = True)
    class Meta:
        model = EmployeeBooking
        fields = '__all__'

class BookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeBooking
        fields = '__all__'

class EmployeeAbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAbsence
        fields = ['id', 'user', 'employee', 'absence_date']
