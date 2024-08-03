# Generated by Django 5.0.6 on 2024-08-01 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='lvl_subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('lvl', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('promocode', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]