from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import ProfileForm, ProfileUpdateForm
from .forms import UserForm_register, UserForm_login, chat_messagesForm
from .models import Profile, FriendRequest, User, chat_messages, Chat, notification


class MessagesView(View):
    def get(self, request, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if request.user in chat.members.all():
                chat.message_set.filter(is_readed=False).exclude(author=request.user).update(is_readed=True)
            else:
                chat = None
        except Chat.DoesNotExist:
            chat = None

        return render(
            request,
            'profile/messages.html',
            {
                'user_profile': request.user,
                'chat': chat,
                'chat_id': chat.id
            }
        )

class CreateDialogView(View):
    def get(self, request, user_id):
        chats = Chat.objects.filter(members__in=[request.user.id, user_id], type=Chat.DIALOG).annotate(c=Count('members')).filter(c=2)
        if chats.count() == 0:
            chat = Chat.objects.create()
            chat.members.add(request.user)
            chat.members.add(user_id)
            notif = notification.objects.create(not_text=f"Новый диалог от {request.user.username}!")
            notif.for_user.add(user_id)
        else:
            chat = chats.first()
        return redirect(reverse('account:messages', kwargs={'chat_id': chat.id}))
class DialogsView(View):
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(request, 'profile/dialog.html', {'user_profile': request.user, 'chats': chats})
@login_required(login_url='account:login')
def create_profile(request):
    try:
        profile = request.user.profile
        # User has a profile, redirect to a specific URL
        return redirect('toons:index')
    except Profile.DoesNotExist:
        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, user=request.user)  # Передайте текущего пользователя
            if profile_form.is_valid():
                profile = profile_form.save()
                return redirect('toons:index')
            # Дополнительные действия после сохранения профиля
        else:
            profile_form = ProfileForm(user=request.user)  # Передайте текущего пользователя для пустой формы

        return render(request, 'profile/profile_create.html', {'form': profile_form})
@login_required(login_url='account:login')
def profile(request):
    try:
        admin_user = User.objects.get(username=request.user.username)
        profile = Profile.objects.get(user=admin_user)
        profile_friend_requests = FriendRequest.objects.filter(to_user=profile.user)
        return render(request, 'profile/profile.html', {'profile': profile, 'profile_friend_requests': profile_friend_requests})
    except Profile.DoesNotExist:
        return redirect('account:profile_create')
@login_required(login_url='account:login')
def friend_FriendRequest(request):
    try:
        profile = request.user.profile
        return render(request, 'profile/profile.html', {'profile': profile})
    except Profile.DoesNotExist:
        return redirect('account:profile_create')

@login_required(login_url='account:login')
def profile_guest(request, slug):
    try:
        profile = Profile.objects.get(slug=slug)
        return render(request, 'profile/profile_guest.html', {'profile': profile})
    except Profile.DoesNotExist:
        return redirect('account:profile_create')
def profile_update(request):
    try:
        profile = request.user.profile
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('account:profile')
        else:
            form = ProfileUpdateForm(instance=request.user.profile)

        return render(request, 'profile/profile_update.html', {'form': form})
    except Profile.DoesNotExist:
        return redirect('account:profile_create')

def register(request):
    form = UserForm_register(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('account:login')
    else:
        form = UserForm_register()
    return render(request, 'account/register.html', {'form': form})


def login_view(request):
    form = UserForm_login()

    if request.user.is_authenticated:
        return redirect('toons:index')

    if request.method == 'POST':

        form = UserForm_login(request.POST, request.FILES)

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('toons:index')
        else:
            return redirect('account:login')
    context = {
        'form': form
    }
    return render(request, 'account/login.html', context)




def logout_view(request):
    logout(request)
    return redirect('account:login')

def send_friend_request(request, slug, *args):
    try:
        profile = Profile.objects.get(slug=slug)
        from_user = request.user  # Get the current user sending the friend request
        to_user = profile.user  # Get the user of the profile being viewed

        friend_request = FriendRequest(from_user=from_user, to_user=to_user)
        friend_request.save()
        return redirect('account:profile')
    except ObjectDoesNotExist:
        # Обработка случая, когда профиль не существует
        return redirect('account:profile_create')

def accept_friend(request, slug, *args):
    try:
        profile = Profile.objects.get(slug=slug)
        friend_request = FriendRequest.objects.get(from_user=profile.user, to_user=request.user)
        friend_request.accept_request(
            accepted=True)  # Update the accept_request method to accept the request with status 'accepted'
        profile.friends.add(friend_request.to_user)
        friend_request.to_user.profile.friends.add(profile.user)
        friend_request.delete()
        return redirect('account:profile')
    except ObjectDoesNotExist:
        # Обработка случая, когда профиль не существует
        return redirect('account:profile_create')

def chat(request):
    user = request.user
    messages = chat_messages.objects.all()  # Initialize messages with an empty queryset
    if request.method == 'POST':
        form = chat_messagesForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            # Redirect back to the same page to allow user to leave another message
            return redirect('account:chat')
    else:
        form = chat_messagesForm(user=user)
    return render(request, 'profile/chat.html', {'form': form, 'messages': messages})

def delete_message(request, message_id):
    user = request.user
    message = chat_messages.objects.get(id=message_id, user=user)
    message.delete()
    return redirect('toons:index')
