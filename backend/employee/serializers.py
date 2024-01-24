from auth_setup.models import User
from rest_framework import serializers
from .models import EmployeeBooking,EmployeeAbsence,Review

class CustomUserserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email","phone_number","profile_photo"]
    
class EmployeeBookingSerializer(serializers.ModelSerializer):
    is_reviewed = serializers.SerializerMethodField()

    userDetails = CustomUserserializer(source = 'user', read_only = True)
    employeeDetails = CustomUserserializer(source = 'employee', read_only = True)
    
    class Meta:
        model = EmployeeBooking
        fields = '__all__'

    def get_is_reviewed(self, obj):
        # Check if there is any review for this user and employee
        is_reviewed = Review.objects.filter(employee=obj.employee, user=obj.user).exists()
        return is_reviewed

class BookingStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeBooking
        fields = '__all__'


class EmployeeAbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAbsence
        fields = ['id', 'user', 'employee', 'absence_date']


class ReviewSerializer(serializers.ModelSerializer):
    userDetails = CustomUserserializer(source = 'user', read_only = True)
    employeeDetails = CustomUserserializer(source = 'employee', read_only = True)
    class Meta:
        model = Review
        fields  = "__all__"