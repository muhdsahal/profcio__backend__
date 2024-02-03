from rest_framework import serializers
from employee.models import EmployeeBooking
from auth_setup.models import User

class EmployeeBookingSalesReportSerializer(serializers.Serializer):
    created_date = serializers.DateField()
    total_sales = serializers.IntegerField()


class BookingEmployeeReportSerializer(serializers.ModelSerializer):
    booking_count = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    pending_count = serializers.SerializerMethodField()
    ongoing_count = serializers.SerializerMethodField()
    completed_count = serializers.SerializerMethodField()

    def get_booking_count(self, obj):
        # Assuming 'bookings' is the related name in User model for the bookings field
        return obj.bookings.count()

    def get_total_price(self, obj):
        employee_id = self.context.get('employee_id')
        bookings = EmployeeBooking.objects.filter(employee=employee_id)
        total_price = sum(booking.price for booking in bookings)
        return total_price

    def get_status_count(self, obj, status):
        employee_id = self.context.get('employee_id')
        bookings = EmployeeBooking.objects.filter(employee=employee_id, booking_status=status)
        return bookings.count()

    def get_pending_count(self, obj):
        return self.get_status_count(obj, 'pending')

    def get_ongoing_count(self, obj):
        return self.get_status_count(obj, 'ongoing')

    def get_completed_count(self, obj):
        return self.get_status_count(obj, 'completed')

    class Meta:
        model = User
        fields = ["id","username","user_type","booking_count","total_price","pending_count","ongoing_count","completed_count"]
