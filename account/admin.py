from django.contrib import admin

from .models import Profile, FriendRequest, chat_messages, Chat, Message, notification


# Register your models here.

admin.site.register(notification)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(FriendRequest)
admin.site.register(chat_messages)