from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/',myTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),

    path('UserRegister/',UserRegister.as_view(),name='UserRegister'),
    path('EmployeeRegister/',EmployeeRegister.as_view(),name='EmployeeRegister'),
    # path('verify/<str:uid64>/<str:token>/', VerifyUserView.as_view(),name='verify-user'), #email verification
    path('auth/verify/<str:uidb64>/<str:token>/', VerifyUserView.as_view(), name='verify-user'),

    # path('verify/<str:uidb64>/<str:token>/', VerifyUserView.as_view(), name='verify-user'),
]
