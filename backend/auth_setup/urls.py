from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView,LogoutView,UserDetailsView

urlpatterns = [
    path('token/',myTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),

    path('register/',UserRegister.as_view(),name='register'),
    path('EmployeeRegister/',EmployeeRegister.as_view(),name='EmployeeRegister'),
    # path('verify/<str:uid64>/<str:token>/', VerifyUserView.as_view(),name='verify-user'), #email verification
    path('auth/verify/<str:uidb64>/<str:token>/', VerifyUserView.as_view(), name='verify-user'),


    path('register/',RegisterView.as_view(),name='rest_register'),
    path('login/',LoginView.as_view(),name='rest_login'),
    path('logout/',UserDetailsView.as_view(),name='rest_user_details')

    
]
