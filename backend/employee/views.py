from django.shortcuts import render
from datetime import datetime
from auth_setup.models import User
from .models import EmployeeBooking,EmployeeAbsence
from .serializers import BookingStatusSerializer, EmployeeBookingSerializer,EmployeeAbsenceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.shortcuts import get_object_or_404
from rest_framework.generics  import RetrieveUpdateAPIView,ListAPIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class BookingEmployeeView(APIView):
    def get(self, request, emp_id):

        queryset = EmployeeBooking.objects.filter(employee=emp_id)
        serializer = EmployeeBookingSerializer(queryset, many=True)
        return Response(serializer.data)
    
# stripe.api_key = config('STRIPE_SECRET_KEY')
stripe.api_key = 'sk_test_51OFqIQSJiD5G4hPsOp9WDdHeFzGx7va82AmGoZfCXQWfdZILiQgIRY87lYDMQxiy4UoPzb79c7LopwQgNW6aNFdH00cGrA0FV7'

@api_view(['POST'])
def create_employee_absence(request):
    serializer = EmployeeAbsenceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_employee_absences(request, emp_id):
    absences = EmployeeAbsence.objects.filter(employee_id=emp_id)
    serializer = EmployeeAbsenceSerializer(absences, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class StripePayment(APIView):
    def post (self,request):
        try:
            data = request.data
            userId = data.get('userId')
            empId = data.get('empId')
            date = data.get('date')
            # print(userId,empId,date,'allllaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            # print(userId,empId,date,'userId,empId,dateuserId       StripePayment')
            # You can use the received data to customize the Stripe session creation
            success_url = f"http://localhost:5173/employeedetails/payment/success/?userId={userId}&empId={empId}&date={date}"

            cancel_url = 'http://localhost:5173/employeedetails/payment/canceled/'
            session =stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': data.get('currency', 'INR'),
                        'product_data': {
                            'name': data.get('name', 'sample'),
                        },
                        'unit_amount': data.get('unit_amount', 100 * 100),
                    },
                    'quantity': data.get('quantity', 1),
                }],
                mode = data.get('mode','payment'),
                success_url = success_url,
                cancel_url = cancel_url, 
                
            )     
            # print(session,'sessssssssssssssssssssssssss')      
            return Response({"message" : session},status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeBookingSubmit(APIView):
    
    def post(self, request):
        try:
            user_id = self.request.data.get('userId')
            employee_id = self.request.data.get('empId')
            date_str = self.request.data.get('date')
            print(date_str, user_id, employee_id, 'all data datestrrrrrrrrrr')

            # Convert the date string to a datetime object without explicit formatting
            date_object = datetime.fromisoformat(date_str)
            print(date_object,'datedateobjectdateobjedctdateobject')
            formatted_date = date_object.date()

            existing_booking = EmployeeBooking.objects.filter(
                user=user_id,
                employee=employee_id,
                booking_date=formatted_date
            ).first()

            if existing_booking:
                return Response({"error": "Booking already exists for this date and plan."}, status=status.HTTP_400_BAD_REQUEST)

            employee = get_object_or_404(User, id=employee_id)
            user = get_object_or_404(User, id=user_id)

            booking = EmployeeBooking(
                user=user, employee=employee, booking_date=formatted_date,is_booked=True)
            booking.save()

            return Response({"message": "Success"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class EmployeeBookingList(ListAPIView):
    queryset = EmployeeBooking.objects.all()
    serializer_class = EmployeeBookingSerializer
    



class BookedByUserID(APIView):
    def get (self,request,*args, **kwargs):
        user_id = kwargs.get('pk')
        try:
            bookings = EmployeeBooking.objects.filter(user=user_id)
        except :
            pass
        serializer = EmployeeBookingSerializer(bookings,many=True)
        if serializer:
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class BookingStatusUpdate(RetrieveUpdateAPIView):
    queryset = EmployeeBooking.objects.all()
    serializer_class = BookingStatusSerializer
    
        
class BookedByEmployeeID(APIView):
    def get (self,request,*args, **kwargs):
        emp_id = kwargs.get('pk')
        try:
            bookings = EmployeeBooking.objects.filter(employee=emp_id)
        except :
            pass
        serializer = EmployeeBookingSerializer(bookings,many=True)
        if serializer:
            return Response(serializer.data)
        else:
            return Response(serializer.errors)