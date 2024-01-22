from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from auth_setup.models import User
from auth_setup.serializers import UserSerializer
from .models import Message

class MessageSerializer(ModelSerializer):
    sender_email=serializers.EmailField(source='sender.email')

    class Meta:
        model = Message
        fields = ['message','sender_email','timestamp']