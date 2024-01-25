from  rest_framework import serializers
from rest_framework_simplejwt.serializers import *
from .models import *


class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = ['id','username','email','profile_photo','user_type','phone_number',
                  'work','place','description','experience','charge','is_active']
        extra_kwargs ={
            'password' : {'write_only':True},
            
        }



class myTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token['email']=user.email
        token['username']= user.username
        token['user_type'] =user.user_type
        token['is_active'] = user.is_active
        token['is_admin'] = user.is_superuser
        return token

class GoogleAuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "passsword"}, write_only=True
    )

    class Meta:
        model = User
        fields = "__all__"

    def save(self):
        user = User(
            username=self._validated_data["username"],
            email=self._validated_data["email"],
            password=self._validated_data["password"],
            is_active=False,
        )
        password = self._validated_data["password"]
        
        if not password :
            raise serializers.ValidationError({"password": "password does not match"})
        user.set_password(password)
        user.save()
        return user    
        
class EmployeedataSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(required=False)

    class Meta:
        model  = User
        fields = ['id','username','email','profile_photo','user_type','phone_number','is_google',
                  'work','place','description','experience','charge','is_active']


 