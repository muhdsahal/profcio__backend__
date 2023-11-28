from  rest_framework import serializers
from rest_framework_simplejwt.serializers import *
from .models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","last_login","is_superuser","first_name","last_name","is_staff","phone_number",
"date_joined","username","email","profile_photo","is_active","user_type","is_google",]
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

class GoogleAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =('id','username','email','password','profile_image',
                 "phone_number",'user_type','is_google','is_active')
        extra_kwargs ={
            'password':{'write_only':True}
        }

class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','username','email','password','profile_image','user_type',
                 "phone_number",'is_google','is_active']
        
class EmployeedataSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id','username','email','profile_photo','user_type','phone_number','is_google',
                  'is_active','work','place','description','experience','charge']