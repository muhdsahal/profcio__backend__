from django.urls import path

from .consumers import ChatConsumer


websocket_urlpatterns=[
    path('ws/chat/<int:id>/',ChatConsumer.as_asgi()),
    # path("ws/notifications/<int:user_id>/", NotificationConsumer.as_asgi()),
    # path('ws/adminnotifications/', AdminNotifications.as_asgi()),
]