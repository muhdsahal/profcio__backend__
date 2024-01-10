from django.urls import path
from .views import *

urlpatterns = [
    path('employee/<int:emp_id>/book/', BookingEmployeeView.as_view(), name='employee_booking'),
    path('employee/booking/register/', EmployeeBookingSubmit.as_view(), name='employee_booking_submit'),
    path('booking/payment/',StripePayment.as_view(), name='stripe-payment'),
    path('employee_bookings_list/', EmployeeBookingList.as_view(), name='employee_bookings_list'),
    path('employee_bookings_list/<int:pk>/', EmployeeBookingListViewById.as_view(), name='employee_bookings_list'),
]
# 