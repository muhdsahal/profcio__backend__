from  rest_framework import serializers
from rest_framework_simplejwt.serializers import *
from .models import User,Service



class UserSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = User
        fields = "__all__"
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
    profile_photo = serializers.ImageField(required=False)

    class Meta:
        model  = User
        fields = ['id','username', 'password','email','profile_photo','user_type','phone_number','is_google',
                  'work','place','description','experience','charge']
        
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'