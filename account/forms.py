from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, chat_messages

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'image', 'birthday', 'user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получите текущего пользователя
        super(ProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user  # Установите текущего пользователя в качестве начального значения
            self.fields['user'].widget = forms.HiddenInput()  # Скрыть поле пользователя в форме

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'image', 'birthday', 'about']
class UserForm_register(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserForm_register, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserForm_login(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class chat_messagesForm(ModelForm):
    class Meta:
        model = chat_messages
        fields = ['user', 'message']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получите текущего пользователя
        super(chat_messagesForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user  # Установите текущего пользователя в качестве начального значения
            self.fields['user'].widget = forms.HiddenInput()  # Скрыть поле пользователя в форме

    def save(self, commit=True):
        user = super(chat_messagesForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class ChatMessage_updateForm(ModelForm):
    class Meta:
        model = chat_messages
        fields = ['user', 'message']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получите текущего пользователя
        super(ChatMessage_updateForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user  # Установите текущего пользователя в качестве начального значения
            self.fields['user'].widget = forms.HiddenInput()  # Скрыть поле пользователя в форме

    def save(self, commit=True):
        user = super(ChatMessage_updateForm, self).save(commit=False)
        if commit:
            user.save()
        return user
