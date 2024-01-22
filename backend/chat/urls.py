from django.urls import path
from . import views
urlpatterns=[
    path('user-previous-chats/<int:user1>/<int:user2>/',views.PrevoiusMessagesView.as_view())

]