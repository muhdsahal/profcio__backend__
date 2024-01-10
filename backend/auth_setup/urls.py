from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView,LogoutView,UserDetailsView
# from django.contrib.auth import views as auth_views


urlpatterns = [
    path('token/',myTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    path('register/',UserRegister.as_view(),name='register'),
    path('employeeregister/',EmployeeRegister.as_view(),name='EmployeeRegister'),
    path('user_block_unblock/<int:pk>/',Userblock.as_view(),name='userblock'),
    path('googleauth/',GoogleAuthentication.as_view(),name='GoogleAuthentication'),
    path('auth/verify/<str:uidb64>/<str:token>/', VerifyUserView.as_view(), name='verify-user'),
    path('password_reset/',PasswordResetAPIView.as_view(), name='password_reset'),
    # path('password_reset_confirm/<str:uidb64>/<str:token>/', PasswordResetAPIView.as_view(), name='password_reset_confirm'),
    path('userdetails/',UserDetails.as_view(),name='user_details'),
    path('password_reset_confirm_validation/<str:uidb64>/<str:token>/',VerifyReset.as_view(),name='password_reset_confirm_validation'),

    path('authentication/',Authentication.as_view(), name='Authentication'),

    path('password_change/',PassWordChange.as_view(),name='password_change'),
    path('user_profile/<int:user_id>/',UserProfile.as_view(),name='userprofile'),

    path('employeelisting/',EmployeeProfileData.as_view(),name='EmployeeListing'),
    path('employeelisting/<int:pk>/',EmployeeProfileDataWithId.as_view(),name='EmployeeListing'),
    
    # path('employee_bookings_list/', EmployeeBookingList.as_view(), name='employee_bookings_list'),
    # # path('employee_bookings_list/<int:id>/', EmployeeBookingList.as_view(), name='employee_bookings_list'),
    # path('employee/<int:emp_id>/book/', BookingEmployeeView.as_view(), name='employee_booking'),
    # path('employee/booking/register/', EmployeeBookingSubmit.as_view(), name='employee_booking_submit'),
    # path('booking/payment/',StripePayment.as_view(), name='stripe-payment'),
    

    path('register/',RegisterView.as_view(),name='rest_register'),
    path('login/',LoginView.as_view(),name='rest_login'),
    path('logout/',UserDetailsView.as_view(),name='rest_user_details'),

    
]
