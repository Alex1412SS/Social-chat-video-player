import random
import string
from datetime import datetime
from time import timezone

from django.db import models
from django.contrib.auth import get_user_model
from numpy import integer
from toons.models import toons_model, Review
from subscribe_payment.models import lvl_subscribe
User = get_user_model()

def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

def rand_key():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, unique=True, blank=True, default=rand_slug)
    nickname = models.CharField(max_length=50)
    about = models.TextField(blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    rating = models.FloatField(default=0.0, blank=True)
    views = models.IntegerField(toons_model, default=0, blank=True, null=True)
    friends = models.ManyToManyField(to=User, related_name='friends', blank=True)
    image = models.ImageField(upload_to='profile', blank=True, default='1670311516_61-fashionhot-club-p-termobele-skins-64.jpg')
    favorites = models.ManyToManyField(to=toons_model, related_name='favorites', blank=True)
    likes_for = models.ManyToManyField(to=toons_model, related_name='likes_for', blank=True)
    likes_reviews = models.ManyToManyField(to=Review, related_name='likes_reviews', blank=True)
    sub = models.ForeignKey(lvl_subscribe, on_delete=models.CASCADE, blank=True, null=True)


    def favorite(self, toons_model):
        self.favorites.add(toons_model)
        self.favorites.add(toons_model)  # Add the toon to the user's profile

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = rand_slug()
        super().save(*args, **kwargs)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Friend Request from {self.from_user} to {self.to_user}"

    def send_request(self):
        # Логика отправки заявки
        friend_request = FriendRequest(from_user=self.from_user, to_user=self.to_user)
        friend_request.save()

    def accept_request(self, accepted=True):
        # Логика принятия заявки
        self.accepted = accepted
        self.save()
class chat_messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = (
        (DIALOG, ('Dialog')),
        (CHAT, ('Chat'))
    )

    type = models.CharField(
        ('Тип'),
        max_length=1,
        choices=CHAT_TYPE_CHOICES,
        default=DIALOG
    )
    members = models.ManyToManyField(User, verbose_name=("Участник"))


    def get_absolute_url(self):
        return 'users:messages', (), {'chat_id': self.pk}


class Message(models.Model):
    chat = models.ForeignKey(Chat, verbose_name=("Чат"), on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name=("Пользователь"), on_delete=models.CASCADE)
    message = models.TextField(("Сообщение"))
    pub_date = models.DateTimeField(('Дата сообщения'), default=datetime.now, blank=True)
    is_readed = models.BooleanField(('Прочитано'), default=False)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.message

class notification(models.Model):
    for_user = models.ManyToManyField(User, related_name='notifications')
    not_text = models.TextField(max_length=200)
    readed = models.BooleanField(default=False)

    def __str__(self):
        return self.not_text + ' / ' + str(self.for_user)

    def readed_notification(self):
        self.readed = True
        self.save()