# Generated by Django 5.0.6 on 2024-07-03 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile_likes_for'),
        ('toons', '0009_review_toons_model_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='likes_reviews',
            field=models.ManyToManyField(blank=True, related_name='likes_reviews', to='toons.review'),
        ),
    ]