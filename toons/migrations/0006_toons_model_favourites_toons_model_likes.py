# Generated by Django 5.0.6 on 2024-07-02 13:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toons', '0005_genre_toons_model_genre'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='toons_model',
            name='favourites',
            field=models.ManyToManyField(blank=True, related_name='favourites', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='toons_model',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='toon_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]