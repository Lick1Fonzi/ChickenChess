"""
ASGI config for ChickenChess project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .routing import ws_urlpatterns
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChickenChess.settings')

#application = get_asgi_application()   #questo va commentato…

application = ProtocolTypeRouter(
 {
 "http" : get_asgi_application(),
 "websocket" : AuthMiddlewareStack(URLRouter(ws_urlpatterns))
 }
)
