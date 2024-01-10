from datetime import datetime
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import  *
from rest_framework import filters
from django.core.exceptions import FieldError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import *
from rest_framework.generics import (
    ListCreateAPIView,RetrieveUpdateDestroyAPIView,
    CreateAPIView,GenericAPIView,ListAPIView,UpdateAPIView,RetrieveUpdateAPIView)
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_str,force_bytes
from django.contrib.auth import get_user_model,authenticate
from verify_email.email_handler import send_verification_email
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from dj_rest_auth.views import LoginView
from rest_framework.decorators import action
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import stripe
from decouple import config
# Create your views here.

class myTokenObtainPairView(TokenObtainPairView):
    serializer_class = myTokenObtainPairSerializer

class UserRegister(CreateAPIView):
    def get_serializer_class(self):
        return UserSerializer
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.set_password(password)
            user.user_type = "user"
            user.save()

            # Generate verification token and UID
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Build verification URL
            verification_url = reverse('verify-user', kwargs={'uidb64': uid, 'token': token})
            verification_url = f'{request.build_absolute_uri(verification_url)}'

            # Send verification email
            subject = 'Profcio | Activate Your Account'
            message = f'Hi {user.username}, Welcome To Profcio..! Click the link to activate your account: {verification_url}'
            from_email = 'sahalshalu830@gmail.com'
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            # Return access and refresh tokens in the response
            return Response(create_jwt_pair_token(user), status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if not user.is_active and default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()

                context = user.user_type
                # Create a JWT token for the user
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                if context == 'employee':
                    redirect_url = 'http://localhost:5173/employee/employee_login/'
                else:
                    redirect_url = 'http://localhost:5173/login/'
                
                return redirect(redirect_url)

        except ObjectDoesNotExist:
            message = 'Activation Link Expired, please register again'
            return JsonResponse({'error': message}, status=400)

        except Exception as e:
            # Handle other exceptions if needed
            message = f'An error occurred during verification: {str(e)}'
            return JsonResponse({'error': message}, status=500)

        return JsonResponse({'error': 'Invalid activation link'}, status=400)



class EmployeeRegister(CreateAPIView):
    def get_serializer_class(self):
        return EmployeedataSerializer
    
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        profile_photo = request.data.get('profile_photo')
        is_active = request.data.get('is_active')
        phone_number = request.data.get('phone_number')
        work = request.data.get('work')
        place = request.data.get('place')
        description = request.data.get('description')
        experience = request.data.get('experience')
        charge = request.data.get('charge')
        profile_photo_file = request.data.get('profile_photo')

        serializer = EmployeedataSerializer(data=request.data) 
         #call data from the Userserializer
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.user_type = "employee"
            user.set_password(request.data.get('password'))
            user.save()

            # creating varification Token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
 
            #createing varification url
            verification_url = reverse('verify-user',kwargs={'uidb64':uid,'token':token})+ f'?context=employee'
            
            #send the varification email
            subject  = 'Profcio | Activate Your Account'
            message = f'Hi {user}, Welcome To Profcio..! click the following link to activate your  account :{request.build_absolute_uri(verification_url)}'
            
            from_email = 'sahalshalu830@gmail.com'
            recipient_list = [user.email]

            try:
                send_mail(subject,message,from_email,recipient_list)
            except Exception as e:
                print(f"Error sending :{e}")
            data = {
                "text":"account created,",
                "status": 200
            }
            return Response(data=data)
        else:
            print('Serializer error are :' ,serializer.errors)
            return Response({'status':'error','msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class PasswordResetAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        user = User.objects.get(email=email)
        # print(user.username,'userrrrrrrrrr')
    

        try:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            # print(uid,token,'uidsuidudiudiudidudiudiudi')
            
            # uid = force_str(urlsafe_base64_decode(uidb64))
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

            print('eeeeeeeeererrrrrrrrrrrrrrror')
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        reset_url = reverse('password_reset_confirm_validation', kwargs={'uidb64':uid,'token':token})
        reset_url = f'{request.build_absolute_uri(reset_url)}'

        subject  = 'Profcio | Reset Your Password'
        message = f'Hi {user} click the following link to reset your  password :{reset_url}'
        

        from_email = 'sahalshalu830@gmail.com'
        recipient_list = [user.email]
        # print(subject, message, from_email, recipient_list)
        send_mail(subject, message, from_email, recipient_list)
        return Response(status=status.HTTP_201_CREATED)
    

class PassWordChange(APIView):

    def post(self, request):
        # Get new password and uid from the request data
        password = request.data.get('new_password')
        uid = request.data.get('uid')

        # Decode the UID
        decoded_id = force_str(urlsafe_base64_decode(uid))

        try: 
            # Retrieve the user
            user = User.objects.get(id=decoded_id)

            # Set the new password using the same hashing mechanism as the abstract user
            user.set_password(password)

            # Save the user to update the password
            user.save()

            print(user.password)
            print(user, "user data is getting")
            print(password, uid, decoded_id, 'passwordpasswordpasswordpasswordpassword')

            return Response(status=status.HTTP_200_OK)

        except User.DoesNotExist:
            # Handle the case where the user with the specified ID is not found
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class VerifyReset(APIView):
    def get(self, request, uidb64, token):
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            context = user.user_type
            print(context,'usertype///////usertype/////usertype')
            if context == 'employee':
                redirect_url = f'http://localhost:5173/employee/reset_password/{uidb64}/{token}'
            else:
                redirect_url = f'http://localhost:5173/reset_password/{uidb64}/{token}'
                
                return redirect(redirect_url)

        except ObjectDoesNotExist:
            message = 'Activation Link Expired, please register again'
            return JsonResponse({'error': message}, status=400)

        except Exception as e:
            # Handle other exceptions if needed
            message = f'An error occurred during verification: {str(e)}'
            return JsonResponse({'error': message}, status=500)


class GoogleAuthentication(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        

        if not User.objects.filter(email=email, is_google=True).exists():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.user_type = "user"
                user.is_active = True
                user.is_google = True
                user.set_password(password)
                user.save()

        user = authenticate(email=email, password=password)

        if user is not None:
            token = create_jwt_pair_token(user)
            response_data = {
                'status': 'Success',
                'msg': 'Registration Successfully',
                'token': token,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'msg': 'Authentication failed'})


def create_jwt_pair_token(user):
    refresh = RefreshToken.for_user(user)
    refresh['email'] = user.email
    refresh['user_type'] = user.user_type
    refresh['is_active'] = user.is_active
    refresh['is_admin'] = user.is_superuser
    refresh['is_google'] = user.is_google

    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return {
        "access": access_token,
        "refresh": refresh_token
    }

class Authentication(APIView):
    permission_classes =(IsAuthenticated,)
    def get(self,request):
        content={'user':str(request.user),'userid':str(request.user.id),'email':str(request.user.email),'is_active':str(request.user.is_active)}
        return Response(content)

class UserDetails(ListAPIView):
    # permission_classes =(IsAuthenticated,)

    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'id', 'email', 'user_type']

                                                          

class Userblock(APIView):
    def put(self,request,*args, **kwargs):
        # get value from url parameter
        value_to_update = kwargs.get('pk')
        if value_to_update is None:
            return Response({'error':'Please Provide a Proper input.'},status=status.HTTP_400_BAD_REQUEST)
        try:
            #retrive user instance based on provided pk
            instance = User.objects.get(pk=value_to_update)
        except User.DoesNotExist:
            return Response({'error':f'user with id={value_to_update} does not exist'},status=status.HTTP_404_NOT_FOUND)
        
        #toggle the value of is_active
        instance.is_active = not instance.is_active
        serializer = UserSerializer(instance,data=request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)


class EmployeeProfileData(ListCreateAPIView):
    queryset = User.objects.filter(user_type='employee')
    serializer_class = EmployeedataSerializer

class EmployeeProfileDataWithId(RetrieveUpdateAPIView):
    queryset = User.objects.filter(user_type='employee')
    serializer_class = EmployeedataSerializer
    
#userprofile class
class UserProfile(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    def get_object(self,user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404
    def get(self,request,user_id):
        user = self.get_object(user_id)
        serializer = self.serializer_class(user)
        return Response(serializer.data)
    def put(self,request,user_id):
        user = self.get_object(user_id)
        serializer = self.serializer_class(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# class BookingEmployeeView(APIView):
#     def get(self, request, emp_id):

#         queryset = EmployeeBooking.objects.filter(employee=emp_id)
#         serializer = EmployeeBookingSerializer(queryset, many=True)
#         return Response(serializer.data)
    
# # stripe.api_key = config('STRIPE_SECRET_KEY')
# stripe.api_key = 'sk_test_51OFqIQSJiD5G4hPsOp9WDdHeFzGx7va82AmGoZfCXQWfdZILiQgIRY87lYDMQxiy4UoPzb79c7LopwQgNW6aNFdH00cGrA0FV7'

# class EmployeeBookingList(ListAPIView):
#     queryset = EmployeeBooking.objects.all()
#     serializer_class = EmployeeBookingSerializer
#     # print(serializer.data,'employeeeEmployeeBookingSerializer')

# class EmployeeBookingList(RetrieveUpdateAPIView):
#     queryset = EmployeeBooking.objects.all()
#     serializer_class = EmployeeBookingSerializer


# class StripePayment(APIView):
#     def post (self,request):
#         try:
#             data = request.data
#             userId = data.get('userId')
#             empId = data.get('empId')
#             date = data.get('date')

#             # print(userId,empId,date,'userId,empId,dateuserId       StripePayment')
#             # You can use the received data to customize the Stripe session creation
#             success_url = f"http://localhost:5173/employeedetails/payment/success/?userId={userId}&empId={empId}&date={date}"

#             cancel_url = 'http://localhost:5173/employeedetails/payment/canceled/'
#             session =stripe.checkout.Session.create(
#                 line_items=[{
#                     'price_data': {
#                         'currency': data.get('currency', 'INR'),
#                         'product_data': {
#                             'name': data.get('name', 'sample'),
#                         },
#                         'unit_amount': data.get('unit_amount', 100 * 100),
#                     },
#                     'quantity': data.get('quantity', 1),
#                 }],
#                 mode = data.get('mode','payment'),
#                 success_url = success_url,
#                 cancel_url = cancel_url, 
                
#             )     
#             # print(session,'sessssssssssssssssssssssssss')      
#             return Response({"message" : session},status=status.HTTP_200_OK)
#         except Exception as e :
#             return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class EmployeeBookingSubmit(APIView):
    
#     def post(self, request):
#         try:
#             user_id = self.request.data.get('userId')
#             employee_id = self.request.data.get('empId')
#             date_str = self.request.data.get('date')
#             print(date_str, user_id, employee_id, 'all data datestrrrrrrrrrr')

#             # Convert the date string to a datetime object without explicit formatting
#             date_object = datetime.fromisoformat(date_str)
#             print(date_object,'datedateobjectdateobjedctdateobject')
#             formatted_date = date_object.date()

#             existing_booking = EmployeeBooking.objects.filter(
#                 user_id=user_id,
#                 employee_id=employee_id,
#                 booking_date=formatted_date
#             ).first()

#             if existing_booking:
#                 return Response({"error": "Booking already exists for this date and plan."}, status=status.HTTP_400_BAD_REQUEST)

#             employee = get_object_or_404(User, id=employee_id)
#             user = get_object_or_404(User, id=user_id)

#             booking = EmployeeBooking(
#                 user=user, employee=employee, booking_date=formatted_date,is_booked=True)
#             booking.save()

#             return Response({"message": "Success"}, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




