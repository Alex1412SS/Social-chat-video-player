# Generated by Django 5.0.6 on 2024-07-21 12:10

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_chat_messages_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat_messages',
            name='slug',
            field=models.SlugField(blank=True, default=account.models.rand_slug, unique=True),
        ),
    ]