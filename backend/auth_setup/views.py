from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import  *
#UserSerializer, myTokenObtainPairSerializer,GoogleAuthSerializer
from . import *
from rest_framework.generics import (
    ListCreateAPIView,RetrieveUpdateDestroyAPIView,
    CreateAPIView,GenericAPIView,ListAPIView,UpdateAPIView)
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
            print(user.pk)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(uid,'<<<<<<<<<<<<<<<<<<<<......>>>>>>>>>>')

            # Build verification URL
            verification_url = reverse('verify-user', kwargs={'uidb64': uid, 'token': token})
            verification_url = f'{request.build_absolute_uri(verification_url)}'


            # Send verification email
            subject = 'Profcio | Activate Your Account'
            message = f'Hi {user.username}, Welcome To Profcio..! Click the link to activate your account: {verification_url}'
            from_email = 'sahalshalu830@gmail.com'  # Replace with your email
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('Serializer errors are:', serializer.errors)
            return Response({'status': 'error', 'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    



class VerifyUserView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)

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
        return UserSerializer
    
    def post(self,request):
        email = request.data.get('email')
        password = request.data.get('password')
        serializer = UserSerializer(data=request.data)  #call data from the Userserializer

        if serializer.is_valid(raise_exception=True):
            user =serializer.save()
            user.user_type = "employee"
            user.set_password(password)
            user.save()

            # creating varification Token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            #createing varification url
            verification_url = reverse('verify-user',kwargs={'uidb64':uid,'token':token}) + f'?context=employee'
            
            #send the varification email
            subject  = 'Profcio | Activate Your Account'
            message = f'Hi {user}, Welcome To Profcio..! click the following link to activate your  account :{request.build_absolute_uri(verification_url)}'
            
            from_email = 'sahalshalu830@gmail.com'
            recipient_list = [user.email]
            send_mail(subject,message,from_email,recipient_list)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            print('Serializer error are :' ,serializer.errors)
            return Response({'status':'error','msg':serializer.error})

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
            return Response({'detail':'password reset successfully...'},status=status.HTTP_200_OK)
        else:
            return Response({'detail':'invalid token or user not found'},status=status.HTTP_400_BAD_REQUEST)
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

class GoogleAuthEmployee(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        

        if not User.objects.filter(email=email, is_google=True).exists():
            serializer = GoogleAuthSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.user_type = "employee"
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
    refresh['is_admin']= user.is_superuser
    refresh['is_google'] = user.is_google

    access_token =str(refresh.access_token)
    refresh_token = str(refresh)

    return{ 
        "access" :access_token,
        "refresh" :refresh_token
    }


class UserDetails(ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    lookup_field = 'id'


# class EmployeeListing(ListAPIView):
#     queryset = User.objects.filter(user_type = 'employee').order_by('id')
#     serializer_class = UserSerializer
#     lookup_field  = 'id'

                                                            

class Userblock(APIView):
    def put(self,request,*args, **kwargs):
        # get value from url parameter
        value_to_update = kwargs.get('pk')
        print(value_to_update,'>>>>>>>>>>>>>>>value_to_update<<<<<<<<<<<<<<<<<<<<<<')
        if value_to_update is None:
            return Response({'error':'Please Provide a Proper input.'},status=status.HTTP_400_BAD_REQUEST)
        try:
            #retrive user instance based on provided pk
            instance = User.objects.get(pk=value_to_update)
            print(instance,'instance>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        except User.DoesNotExist:
            return Response({'error':f'user with id={value_to_update} does not exist'},status=status.HTTP_404_NOT_FOUND)
        
        #toggle the value of is_active
        instance.is_active = not instance.is_active
        print(instance)
        serializer = UserSerializer(instance,data=request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)


class EmployeeProfileData(ListCreateAPIView):
    queryset =User.objects.filter(user_type='employee')
    serializer_class = EmployeedataSerializer

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer