from  rest_framework import serializers
from rest_framework_simplejwt.serializers import *
from .models import *


class UserSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(allow_null=True, required=False)

    class Meta:
        model = User
        fields = ['id','username','email','profile_photo','user_type','phone_number',
                  'work','place','description','experience','charge']
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
    password = serializers.CharField(
        style={"input_type": "passsword"}, write_only=True
    )
    # class Meta:
    #     model = User
    #     fields =('id','username','email','profile_photo',
    #              "phone_number",'user_type','is_google','is_active','password')
    #     # extra_kwargs ={
    #     #     'password':{'write_only':True}
    #     # }
    # password2 = serializers.CharField(
    #     style={"input_type": "passsword"}, write_only=True
    # )

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
class EditUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','username','email','profile_image','user_type',
                 "phone_number",'is_google','is_active']
        
class EmployeedataSerializer(serializers.ModelSerializer):
    profile_photo = serializers.ImageField(required=False)

    class Meta:
        model  = User
        fields = ['id','username','email','profile_photo','user_type','phone_number','is_google',
                  'work','place','description','experience','charge']




# class CustomUserserializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username','email','phone_number']

# class EmployeeBookingSerializer(serializers.ModelSerializer):
#     userDetails = CustomUserserializer(source = 'user', read_only = True)
#     employeeDetails = CustomUserserializer(source = 'employee', read_only = True)
#     class Meta:
#         model = EmployeeBooking
#         fields = '__all__'
 