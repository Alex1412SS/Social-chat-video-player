# Generated by Django 5.0.6 on 2024-08-01 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscribe_payment', '0001_initial'),
        ('toons', '0013_toons_model_sub_lvl'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toons_model',
            name='sub_lvl',
        ),
        migrations.AddField(
            model_name='toons_model',
            name='subing',
            field=models.ManyToManyField(blank=True, related_name='subing', to='subscribe_payment.lvl_subscribe'),
        ),
    ]
