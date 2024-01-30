from django.urls import path

from .consumers import ChatConsumer,Notification_Consumer


websocket_urlpatterns=[
    path('ws/chat/<int:id>/',ChatConsumer.as_asgi()),
    path("ws/notifications/", Notification_Consumer.as_asgi()),
    # path('ws/adminnotifications/', AdminNotifications.as_asgi()),
]