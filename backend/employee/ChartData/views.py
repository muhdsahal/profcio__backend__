from employee.models import EmployeeBooking
from auth_setup.models import User
from rest_framework import generics
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from django.db.models import Sum,Count
from .serializers import BookingEmployeeReportSerializer
from employee.serializers import EmployeeBookingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from fpdf import FPDF
from rest_framework import generics

#total users count
class UserCountApiView(generics.RetrieveAPIView):
    def get(self,request,*args, **kwargs):
        all_user = User.objects.exclude(is_superuser=True).count()
        user_count = User.objects.filter(user_type='user').count()
        employee_count = User.objects.filter(user_type='employee').count()
        response_data = {
            'users':[all_user,user_count,employee_count]
        }
        
        return Response(response_data)


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
        return Response(response_data)
    
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
        employee = self.kwargs.get('employee')
        status = self.request.query_params.get('booking_status')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if status=='all' and  start_date=='' and end_date=='':
            queryset = EmployeeBooking.objects.filter(employee=employee)
            return queryset
        
        elif status!= 'all'  and start_date != ''  and end_date!= '':
            queryset = EmployeeBooking.objects.filter(created_date__range=(start_date,end_date),employee=employee,booking_status=status)
            return queryset
        
        elif status== 'all'  and start_date != ''  and end_date!= '':
            queryset = EmployeeBooking.objects.filter(created_date__range=(start_date,end_date),employee=employee)
            return queryset
        elif status!= 'all'  and start_date == ''  and end_date== '':
            queryset = EmployeeBooking.objects.filter(booking_status=status,employee=employee)
            return queryset

class SalesReportPDFView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = HttpResponse(content_type='application/pdf')
        filename = 'Expenses_' + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.pdf'
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

        w_pt =8.5*50
        h_pt =11*20
        pdf = FPDF(format=(w_pt,h_pt))
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Sales Report", ln=True, align='C')
        pdf.cell(200, 10, txt=str(datetime.now()), ln=True, align='C')
        col_names = ['Id', 'Client', 'Email', 'Phone number', 'Booking date', 'Price', 'Status']
        col_widths = [20, 40, 70, 40, 30, 30, 40]
        for i, name in enumerate(col_names):
            pdf.cell(col_widths[i], 10, name, border=1)
        pdf.ln()
        for obj in queryset:
            serializer = EmployeeBookingSerializer(obj)
            data_row = [
                serializer.data['id'],
                serializer.data['userDetails']['username'],
                serializer.data['userDetails']['email'],
                serializer.data['userDetails']['phone_number'],
                serializer.data['booking_date'],
                serializer.data['price'],
                serializer.data['booking_status']
            ]
            for i, item in enumerate(data_row):
                pdf.cell(col_widths[i], 10, str(item), border=1)
            pdf.ln()

        response.write(pdf.output(dest='S').encode('latin1'))
        return response

    def get_queryset(self):
        employee = self.kwargs.get('employee')
        status = self.request.query_params.get('booking_status')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        queryset = EmployeeBooking.objects.filter(employee=employee)

        if status != 'all':
            queryset = queryset.filter(booking_status=status)
        if start_date and end_date:
            queryset = queryset.filter(created_date__range=(start_date, end_date))

        return queryset
    

class SalesReportViewAdmin(generics.ListAPIView):
    serializer_class = EmployeeBookingSerializer
    def get_queryset(self):
        status = self.request.query_params.get('booking_status')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if status=='all' and  start_date=='' and end_date=='':
            queryset = EmployeeBooking.objects.all()
            return queryset
        
        elif status!= 'all'  and start_date != ''  and end_date!= '':
            queryset = EmployeeBooking.objects.filter(created_date__range=(start_date,end_date),booking_status=status)
            return queryset
        
        elif status== 'all'  and start_date != ''  and end_date!= '':
            queryset = EmployeeBooking.objects.filter(created_date__range=(start_date,end_date))
            return queryset
        elif status!= 'all'  and start_date == ''  and end_date== '':
            queryset = EmployeeBooking.objects.filter(booking_status=status)
            return queryset


class SalesReportPDFAdminView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = HttpResponse(content_type='application/pdf')
        filename = 'Expenses_' + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + '.pdf'
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

        w_pt =8.5*50
        h_pt =11*20
        pdf = FPDF(format=(w_pt,h_pt))
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Sales Report", ln=True, align='C')
        pdf.cell(200, 10, txt=str(datetime.now()), ln=True, align='C')
        col_names = ['Id', 'Client', 'Email', 'Phone number', 'Booking date', 'Price', 'Status']
        col_widths = [20, 40, 70, 40, 30, 30, 40]
        for i, name in enumerate(col_names):
            pdf.cell(col_widths[i], 10, name, border=1)
        pdf.ln()
        for obj in queryset:
            serializer = EmployeeBookingSerializer(obj)
            data_row = [
                serializer.data['id'],
                serializer.data['userDetails']['username'],
                serializer.data['userDetails']['email'],
                serializer.data['userDetails']['phone_number'],
                serializer.data['booking_date'],
                serializer.data['price'],
                serializer.data['booking_status']
            ]
            for i, item in enumerate(data_row):
                pdf.cell(col_widths[i], 10, str(item), border=1)
            pdf.ln()

        response.write(pdf.output(dest='S').encode('latin1'))
        return response

    def get_queryset(self):
        status = self.request.query_params.get('booking_status')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        queryset = EmployeeBooking.objects.all()

        if status != 'all':
            queryset = queryset.filter(booking_status=status)
        if start_date and end_date:
            queryset = queryset.filter(created_date__range=(start_date, end_date))

        return queryset