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
        # Handle file upload for profile photo
        profile_photo_file = request.data.get('profile_photo')

        # if profile_photo_file:
        #     file_name = default_storage.save(f'images/profile/{profile_photo_file.name}', ContentFile(profile_photo_file.read()))
        #     profile_photo_path = default_storage.url(file_name)
        #     request.data['profile_photo'] = profile_photo_path

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

class ForgotPasswordView(APIView):
    def post(self,request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail':'User not Found'},status=status.HTTP_404_NOT_FOUND)
        
        #generate reset token and UID
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        #Build reset URL
        reset_url= reverse('password_reset',kwargs={'uid64':uid,'token':token})
        reset_url = request.build_absolute_uri(reset_url)

        # Send password reset email
        subject = 'Profcio | Password Reset'
        message = f'Hi {user.username}, To reset your password, click the link: {reset_url}'
        from_email = 'sahalshalu830@gmail.com'  # Replace with your email
        recipient_list = [user.email]

        send_mail(subject,message,from_email,recipient_list)

        return Response({'detail':'Password reset email sent'},status=status.HTTP_200_OK)

#reset password
class PasswordResetView(APIView):
    def post(self,request,uidb64,token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError,ValueError,OverflowError,User.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user,token):
            #token is valid ,allow the user reset password
            new_password = request.data.get('new_password')

            #set the new password
            user.set_password(new_password)
            user.save()

            # log the user in (optional)
            login = LoginView
            login(request,user)
            return Response({'detail':'password reset successfully...'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'detail':'invalid token or user not found'},
                            status=status.HTTP_400_BAD_REQUEST)
        


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


class CategoryService(ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

class CategoryRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    

class ServiceListCreateView(ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category']

    
class ServiceRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

# class EmployeeBookingView(ListCreateAPIView):
#     queryset = EmployeeBooking.objects.all()
#     serializer_class = EmployeeBookingSerializer

# class EmployeeDetailView(APIView):
#     def get(self, request, emp_id):
#         employee = get_object_or_404(User, id=emp_id)
#         availability = WeeklyAvailability.objects.filter(employee=employee).values('day_of_week', 'is_available')
#         serializer = EmployeedataSerializer(employee)
#         return Response({**serializer.data, 'availability': availability})

# class AvailableTimeSlotsView(APIView):
#     def get(self, request, emp_id, date):
#         employee = get_object_or_404(User, id=emp_id)
#         # Check if any existing booking overlaps with the requested date
#         existing_bookings = EmployeeBooking.objects.filter(booking_dates__contains=date.strftime('%Y-%m-%d'))
#         is_available = WeeklyAvailability.objects.filter(
#             employee=employee, day_of_week=date.weekday() + 1  # Adjust for weekday indexing
#         ).exists() and not existing_bookings.exists()
#         return Response({'is_available': is_available})

# class EmployeeBookingView(APIView):
#     def post(self, request, emp_id):
#         data = request.data
#         data['employee'] = emp_id
#         serializer = EmployeeBookingSerializer(data=data)
#         if serializer.is_valid():
#             try:
#                 selected_dates = self.validate_booking_dates(serializer.validated_data['booking_dates'])
#                 if len(selected_dates) < 3 or len(selected_dates) > 7:
#                     raise ValueError("Number of selected days must be between 3 and 7")
#                 booking_dates = ','.join(selected_dates)
#                 serializer.validated_data['booking_dates'] = booking_dates
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             except Exception as e:
#                 return Response({'error':
 
#             str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def validate_booking_dates(self, booking_dates_str):
#         selected_dates = []
#         for date_str in booking_dates_str.split(','):
#             selected_dates.append(datetime.datetime.strptime(date_str.strip(), '%Y-%m-%d').date())
#         return selected_dates

# ... other views for authentication, authorization, etc.
 

class BookingEmployeeView(APIView):
    def get(self, request, emp_id):

        queryset = EmployeeBooking.objects.filter(employee=emp_id)
        serializer = EmployeeBookingSerializer(queryset, many=True)
        return Response(serializer.data)

class EmployeeBookingSubmit(APIView):
    
    def post (self,request):
        try:
            user_id = self.request.data.get('userId')
            employee_id = self.request.data.get('employeeId')
            date_str = self.request.data.get('date')

            date_str = str(date_str)

            date_object = datetime.strptime(date_str, '%Y-%m-%d')

            formatted_date = date_object.date()

            print(date_str,'formatted_date')
            existing_booking = EmployeeBooking.objects.filter(
                user_id = user_id,
                employee_id = employee_id,
                booking_date = formatted_date
            ).first()
            
            if existing_booking:
                    return Response({"error": "Booking already exists for this date and plan."}, status=status.HTTP_400_BAD_REQUEST)

            employee = get_object_or_404(User,id=employee_id)
            user = get_object_or_404(User, id=user_id)

            booking = EmployeeBooking(
                user=user,employee=employee,booking_date=formatted_date)
            booking.save()

            return Response({"message": "Success"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
