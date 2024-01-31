from django.urls import path
from .views import *

urlpatterns = [
    path('admin/usercount/',UserCountApiView.as_view(),name='user_count'),
    path('admin/booking_detials/',BookingDetialsApi.as_view(),name='booking_detials'),
    path('check/<int:employee_id>/', BookingCountApi.as_view())
]
