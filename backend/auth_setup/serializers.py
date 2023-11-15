from  rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User,EmployeeDetail,UserDetail



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','username','email','password','profile_photo','user_type']
        extra_kwargs ={
            'password' : {'write_only':True},
        }



class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token['email']=user.email
        token['user_type'] =user.user_type
        token['is_active'] = user.is_active
        token['is_admin'] = user.is_superuser

        return token