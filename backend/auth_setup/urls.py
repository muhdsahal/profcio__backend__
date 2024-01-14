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
    path('user_block_unblock/<int:pk>/',Userblock.as_view(),name='userblock'),
    path('googleauth/',GoogleAuthentication.as_view(),name='GoogleAuthentication'),
    path('auth/verify/<str:uidb64>/<str:token>/', VerifyUserView.as_view(), name='verify-user'),
    path('password_reset/',PasswordResetAPIView.as_view(), name='password_reset'),
    path('password_change/',PassWordChange.as_view(),name='password_change'),
    # path('password_reset_confirm/<str:uidb64>/<str:token>/', PasswordResetAPIView.as_view(), name='password_reset_confirm'),
    path('userdetails/',UserDetails.as_view(),name='user_details'),
    path('password_reset_confirm_validation/<str:uidb64>/<str:token>/',VerifyReset.as_view(),name='password_reset_confirm_validation'),
    path('authentication/',Authentication.as_view(), name='Authentication'),
    path('user_profile/<int:user_id>/',UserProfile.as_view(),name='userprofile'),
    path('employeelisting/',EmployeeProfileData.as_view(),name='EmployeeListing'),
    path('employeelisting/<int:pk>/',EmployeeProfileDataWithId.as_view(),name='EmployeeListing'),
    path('register/',RegisterView.as_view(),name='rest_register'),
    path('login/',LoginView.as_view(),name='rest_login'),
    path('logout/',LogoutView.as_view(),name='logout'),

    
]
