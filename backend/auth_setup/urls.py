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
    path('forgot_password/',ForgotPasswordView.as_view(),name='forgot_password'),
    path('reset_password/<str:uidb64>/<str:token>/',PasswordResetView.as_view(),name='reset_password'),
    path('userdetails/',UserDetails.as_view(),name='user_details'),

    path('authentication/',Authentication.as_view(), name='Authentication'),
    path('service_category/',CategoryService.as_view(),name='service_category'),
    path('service_category/<int:pk>',CategoryRetrieveUpdateView.as_view(),name='service_category'),
    path('services/', ServiceListCreateView.as_view(), name='service-list-create'),
    path('services/<int:pk>/', ServiceRetrieveUpdateView.as_view(), name='service-retrieve-update'),
    # path('service-categories/', ServiceCategoryChoicesView.as_view(), name='service-category-choices'),

    path('user_profile/<int:user_id>/',UserProfile.as_view(),name='userprofile'),

    path('employeelisting/',EmployeeProfileData.as_view(),name='EmployeeListing'),
    path('employeelisting/<int:pk>/',EmployeeProfileDataWithId.as_view(),name='EmployeeListing'),
    # path('employees/<int:emp_id>/', EmployeeDetailView.as_view(), name='employee-detail'),
    # path('employees/<int:emp_id>/available/<str:date>/', AvailableTimeSlotsView.as_view(), name='employee-available'),
    path('employee/<int:emp_id>/book/', BookingEmployeeView.as_view(), name='employee_booking'),
    path('employee/booking/register/', EmployeeBookingSubmit.as_view(), name='employee_booking_submit'),
    
    

    path('register/',RegisterView.as_view(),name='rest_register'),
    path('login/',LoginView.as_view(),name='rest_login'),
    path('logout/',UserDetailsView.as_view(),name='rest_user_details'),

    
]
