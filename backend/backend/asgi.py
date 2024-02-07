"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()



import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Get the Django ASGI application
django_asgi_application = get_asgi_application()

# WebSocket application
websocket_application = AuthMiddlewareStack(
    URLRouter(chat.routing.websocket_urlpatterns)
)

# Combined application for both HTTP and WebSocket
application = ProtocolTypeRouter(
    {
        "http": django_asgi_application,
        "websocket": websocket_application,
    }
)