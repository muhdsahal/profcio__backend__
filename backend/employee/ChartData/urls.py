from django.urls import path
from .views import *

urlpatterns = [
    path('admin/usercount/',UserCountApiView.as_view(),name='user_count'),
    path('admin/booking_detials/',BookingDetialsApi.as_view(),name='booking_detials'),
    path('booking_report_emp/<int:employee_id>/', BookingReportEmployeeApi.as_view(),name='booking_report_emp'),
    path('sales_report_admin/', SalesReportViewAdmin.as_view(),name='SalesReportViewAdmin'),
    path('sales_report/<int:employee>/', SalesReportView.as_view(),name='SalesReportView'),
    path('sales_report_pdf/<int:employee>/', SalesReportPDFView.as_view(), name='sales_report_pdf'),
    path('sales_report_pdf_admin/', SalesReportPDFAdminView.as_view(), name='sales_report_pdf-admin'),
]
