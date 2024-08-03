from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import Avg
import random
import string
from subscribe_payment.models import lvl_subscribe

User = get_user_model()
from django.urls import reverse


#создание случайного имени
def rand_slug():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

#класс категории
class category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = rand_slug()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('toons:category_detail', kwargs={'slug': self.slug})
class authors(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = rand_slug()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def get_absolute_url(self):
        return reverse('toons:author_detail', kwargs={'slug': self.slug})
class genre(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = rand_slug()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def get_absolute_url(self):
        return reverse('toons:genre_detail', kwargs={'slug': self.slug})
class Review_review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=2000)
    likes = models.ManyToManyField(to=User, related_name='review_review_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def likes_count(self):
        return self.likes.count()
    def unlike(self, user):
        self.likes.remove(user)
    def like(self, user):
        self.likes.add(user)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    likes = models.ManyToManyField(to=User, related_name='review_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    otvet = models.ManyToManyField(Review_review, related_name='reviews', blank=True)

    def likes_count(self):
        return self.likes.count()
    def unlike(self, user):
        self.likes.remove(user)
    def like(self, user):
        self.likes.add(user)


#класс мультиков)(()()))
class toons_model(models.Model):
    genre = models.ForeignKey(genre, on_delete=models.CASCADE, verbose_name='Жанр', blank=True, null=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    author = models.ForeignKey(authors, on_delete=models.CASCADE, verbose_name='Автор', blank=True, null=True)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='toons', blank=True, default='1670311516_61-fashionhot-club-p-termobele-skins-64.jpg')
    rating = models.FloatField(default=0.0, blank=True)
    year_created = models.DateField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    views = models.IntegerField(default=0)  # Новое поле для просмотров
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(to=User, related_name='toon_likes', blank=True, default='alex')
    favourites = models.ManyToManyField(to=User, related_name='favourites', blank=True)
    reviews = models.ManyToManyField(to=Review, related_name='reviews', blank=True)
    subing = models.ForeignKey(lvl_subscribe, on_delete=models.DO_NOTHING, related_name='subing', blank=True, null=True)

    def reviews_cycle(self):
        return self.reviews.order_by('-created_at')

    def get_rating(self):
        return self.reviews.aggregate(Avg('rating'))['rating__avg']


    def favourite(self, user):
        self.favourites.add(user)

    def unfavourite(self, user):
        self.favourites.remove(user)

    def like(self, user):
        self.likes.add(user)

    def unlike(self, user):
        self.likes.remove(user)

    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = rand_slug()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Мультик'
        verbose_name_plural = 'Мультики'

    def increase_views(self):
        self.views += 1
        self.save()

    # Логика для увеличения просмотров при посещении страницы
    def visit(self):
        self.increase_views()

    def get_absolute_url(self):
        return reverse('toons:toons_detail', kwargs={'slug': self.slug})


class toon_series(models.Model):
    toon = models.ForeignKey(toons_model, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    video = models.FileField(upload_to='video/', validators=[FileExtensionValidator(allowed_extensions=['mp4'])], blank=True, default='1670311516_61-fashionhot-club-p-termobele-skins-64.jpg', null=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    year_created = models.DateField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = rand_slug()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'
