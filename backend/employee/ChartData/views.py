from employee.models import EmployeeBooking
from auth_setup.models import User
from rest_framework import generics
from django.http import Http404, JsonResponse
from django.db.models import Sum,Count
from .serializers import BookingEmployeeReportSerializer
from employee.serializers import EmployeeBookingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
#total users count
class UserCountApiView(generics.RetrieveAPIView):
    def get(self,request,*args, **kwargs):
        all_user = User.objects.exclude(is_superuser=True).count()
        user_count = User.objects.filter(user_type='user').count()
        employee_count = User.objects.filter(user_type='employee').count()
        response_data = {
            'users':[all_user,user_count,employee_count]
        }
        
        return JsonResponse(response_data)


class BookingDetialsApi(generics.RetrieveAPIView):
    def get(self,request,*args, **kwargs):

        Booking_count = EmployeeBooking.objects.all().count()
        Booking_pending = EmployeeBooking.objects.filter(booking_status='pending').count()
        Booking_ongoing = EmployeeBooking.objects.filter(booking_status='ongoing').count()
        Booking_completed = EmployeeBooking.objects.filter(booking_status='completed').count()
        # most_booked_employee = User.objects.annotate(num_bookings=Count('employee')).order_by('-num_bookings').first()
        total_price = EmployeeBooking.objects.all().aggregate(total_price=Sum('price'))
        response_data = {
            'data':[Booking_count,Booking_pending,Booking_ongoing,Booking_completed,total_price]
        }
        return JsonResponse(response_data)
    
class BookingReportEmployeeApi(generics.RetrieveUpdateAPIView):
    serializer_class = BookingEmployeeReportSerializer

    def get_queryset(self):
        employee_id = self.kwargs['employee_id']
        return User.objects.filter(id=employee_id, user_type='employee')

    def get_object(self):
        queryset = self.get_queryset()
        obj = queryset.first()
        if obj is None:
            raise Http404("Employee not found")
        return obj

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['employee_id'] = self.kwargs['employee_id']
        return context
    

class SalesReportView(generics.ListAPIView):
    serializer_class = EmployeeBookingSerializer
    def get_queryset(self):

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date and end_date and start_date != end_date:
            queryset = EmployeeBooking.objects.filter(created_date__range=(start_date,end_date))
            return queryset
