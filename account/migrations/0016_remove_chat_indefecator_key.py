# Generated by Django 5.0.6 on 2024-07-30 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_chat_indefecator_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='indefecator_key',
        ),
    ]