from django.urls import path
from .views import *

urlpatterns = [
    path('service_category/',ServiceCategoryView.as_view() ,name='service_category'),
    path('service_category/<int:pk>',ServiceCategoryViewById.as_view() ,name='service_category_id'),
    path('service_list/',ServiceView.as_view() ,name='service_list'),
    path('service_list/<int:pk>/',ServiceViewById.as_view() ,name='service_list_id'),
]