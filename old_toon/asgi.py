# asgi.py

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import account.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'old_toon.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            account.routing.websocket_urlpatterns
        )
    ),
})