from django import forms
from django.forms import ModelForm
from .models import toons_model, Review

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получите текущего пользователя
        super(ReviewForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user  # Установите текущего пользователя в качестве начального значения
            self.fields['user'].widget = forms.HiddenInput()  # Скрыть поле пользователя в форме

    def save(self, commit=True):
        user = super(ReviewForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class UpdateReview(ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получите текущего пользователя
        super(UpdateReview, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user  # Установите текущего пользователя в качестве начального значения
            self.fields['user'].widget = forms.HiddenInput()  # Скрыть поле пользователя в форме

    def save(self, commit=True):
        user = super(UpdateReview, self).save(commit=False)
        if commit:
            user.save()
        return user