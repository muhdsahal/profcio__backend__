from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView,LogoutView,UserDetailsView

urlpatterns = [
    path('token/',myTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
 
    path('register/',UserRegister.as_view(),name='register'),
    path('employeeregister/',EmployeeRegister.as_view(),name='EmployeeRegister'),
    
    # path('verify/<str:uid64>/<str:token>/', VerifyUserView.as_view(),name='verify-user'), #email verification
    path('user_block_unblock/<int:pk>/',Userblock.as_view(),name='userblock'),
    path('googleauth/',GoogleAuthentication.as_view(),name='GoogleAuthentication'),
    path('auth/verify/<str:uidb64>/<str:token>/', VerifyUserView.as_view(), name='verify-user'),
    path('forgot_password/',ForgotPasswordView.as_view(),name='forgot_password'),
    path('reset_password/<str:uidb64>/<str:token>/',PasswordResetView.as_view(),name='reset_password'),
    path('userdetails/',UserDetails.as_view(),name='user_details'),
    path('services/', ServiceListCreateView.as_view(), name='servicelistcreate'),

    path('user_profile/<int:user_id>/',UserProfile.as_view(),name='userprofile'),

    path('employeelisting/',EmployeeProfileData.as_view(),name='EmployeeListing'),

    path('register/',RegisterView.as_view(),name='rest_register'),
    path('login/',LoginView.as_view(),name='rest_login'),
    path('logout/',UserDetailsView.as_view(),name='rest_user_details'),

    
]
