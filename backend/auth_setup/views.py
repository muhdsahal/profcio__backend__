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
from django.db import IntegrityError
import stripe
from decouple import config
from social_django.utils import psa
from django.contrib.auth import get_user_model
import requests

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
            from_email = 'profcioweb@gmail.com'
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
                    redirect_url = 'http://localhost:5173/employee_login/'
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


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response (status=status.HTTP_400_BAD_REQUEST)
        
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
            
            from_email = 'profcioweb@gmail.com'
            recipient_list = [user.email]

            try:
                send_mail(subject,message,from_email,recipient_list)
            except Exception as e:
                Response(f"Error sending :{e}")
            data = {
                "text":"account created,",
                "status": 200
            }
            return Response(data=data)
        else:
            return Response({'status':'error','msg':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class PasswordResetAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'detail': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(email=email)
    
        try:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.id))

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
        reset_url = reverse('password_reset_confirm_validation', kwargs={'uidb64':uid,'token':token})
        reset_url = f'{request.build_absolute_uri(reset_url)}'

        subject  = 'Profcio | Reset Your Password'
        message = f'Hi {user} click the following link to reset your  password :{reset_url}'
        

        from_email = 'profcioweb@gmail.com'
        recipient_list = [user.email]
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
            return Response(status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class VerifyReset(APIView):
    def get(self, request, uidb64, token):
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            context = user.user_type
            if context == 'employee':
                redirect_url = f'http://localhost:5173/employee/reset_password/{uidb64}/{token}'
            else:
                redirect_url = f'http://localhost:5173/reset_password/{uidb64}/{token}'
                
            return redirect(redirect_url)

        except ObjectDoesNotExist:
            message = 'Activation Link Expired, please register again'
            return JsonResponse({'error': message}, status=400)

        except Exception as e:
            message = f'An error occurred during verification: {str(e)}'
            return JsonResponse({'error': message}, status=500)



class GoogleSignup(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not User.objects.filter(email=email).exists():
            serializer = GoogleAuthSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
            user.user_type = "user"
            user.is_active = True
            user.is_google = True
            user.save()
            data = {
                "Text": "Your google SignUp successfully!",
                "signup": "signup",
                "status": 200,
                }
            return Response(data=data)
        if User.objects.filter(email=email).exists():
            data = {
                "Text": "This Email alredy exist!",
                "status": 403,
            }
            return Response(data=data)
        else:
            data = {"Text":serializer.errors,"status":404}
            return Response(data=data)

class GoogleLogin(APIView):
     def post(self, request):
        email = request.data.get("email")

        if User.objects.filter(email=email).exists():
            access_token = request.data.get("access_token")
            Googleurl = config("GOOGLE_VERIFY")
            get_data = f"{Googleurl}access_token={access_token}"
            response = requests.get(get_data)

            if response.status_code == 200:
                user_data = response.json()
                check_email = user_data["email"]
                if check_email == email:
                    user = User.objects.get(email=email)
                    token = RefreshToken.for_user(user)
                    token["email"] = user.email
                    token["is_active"] = user.is_active
                    token["is_superuser"] = user.is_superuser
                    token["user_type"] = user.user_type
                    token["is_google"] = user.is_google
                    dataa = {
                        "refresh": str(token),
                        "access": str(token.access_token),
                    }

                    if user.is_active:
                        data = {
                            "message": "Your Login successfully! ",
                            "status": 201,
                            "token": dataa,
                        }
                    else:
                        data = {
                            "message": "Your Account has been blocked ! ",
                            "status": 202,
                            "token": dataa,
                        }

                    return Response(data=data)
            else:
                data = {
                    "message": response.text,
                    "status": 406,
                }
                return Response(data=data)
        else:
            data = {
                "message": "This Email have no account please Create new account! ",
                "status": 403,
            }
            return Response(data=data)


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


class UserDetails(ListAPIView):
    queryset = User.objects.exclude(is_superuser=True).order_by("id")
    serializer_class = UserSerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'id', 'email', 'user_type']

class Userblock(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class =UserSerializer                                                         

class EmployeeProfileData(ListCreateAPIView):
    
    queryset = User.objects.filter(user_type='employee')
    serializer_class = EmployeedataSerializer

class EmployeeProfileDataWithId(RetrieveUpdateAPIView):
    queryset = User.objects.filter(user_type='employee')
    serializer_class = EmployeedataSerializer
    


class UserProfile(RetrieveUpdateAPIView):
    
    serializer_class = UserSerializer
    def get_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, user_id):
        user = self.get_object(user_id)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def put(self, request, user_id):
        user = self.get_object(user_id)
        serializer = self.serializer_class(user, data=request.data)
        
        if serializer.is_valid():
            if 'is_active' not in request.data:
                serializer.validated_data['is_active'] = user.is_active
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, user_id):
        user = self.get_object(user_id)
        serializer = self.serializer_class(user, data=request.data)
        
        if serializer.is_valid():
            if 'is_active' not in request.data:
                serializer.validated_data['is_active'] = user.is_active

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)