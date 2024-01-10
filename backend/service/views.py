from django.shortcuts import render
from .serializers import ServiceCategorySerializer,ServiceSerializer
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateAPIView
from .models import ServiceCategory,Service
from rest_framework import filters
from rest_framework.views import APIView

# Create your views here.

class ServiceCategoryView(ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

class ServiceCategoryViewById(RetrieveUpdateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer


class ServiceView(ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category']

    
class ServiceViewById(RetrieveUpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer