# routing.py

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/', consumers.ChatMessagesConsumer.as_asgi()),
    re_path(r'ws/chat2/', consumers.private_chat.as_asgi()),
    re_path(r'ws/reviews/', consumers.reviews.as_asgi()),
]