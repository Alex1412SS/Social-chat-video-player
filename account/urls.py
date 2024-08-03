from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import url
from django.urls import path, include
from django.views.generic import TemplateView

from . import views
from .consumers import ChatMessagesConsumer

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('delete_message/<int:message_id>', views.delete_message, name='delete_message'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile_create/', views.create_profile, name='profile_create'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('profile_guest/<slug:slug>', views.profile_guest, name='profile_guest'),
    path('logout/', views.logout_view, name='logout'),
    path('send_friend/<slug:slug>', views.send_friend_request, name='send_friend'),
    path('accept_friend/<slug:slug>', views.accept_friend, name='accept_friend'),
    path('', views.chat, name='indsex'),
    path(r'^dialogs/$', login_required(views.DialogsView.as_view()), name='dialog'),
    path(r'^dialogs/(?P<chat_id>\d+)/$', login_required(views.MessagesView.as_view()), name='messages'),
    path(r'^dialogs/create/(?P<user_id>\d+)/$', login_required(views.CreateDialogView.as_view()), name='create_dialog'),

]
