# Generated by Django 4.2.4 on 2023-08-18 15:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_buddyship_user_buddyships'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='buddyships',
            field=models.ManyToManyField(related_name='related_to+', through='authentication.Buddyship', to=settings.AUTH_USER_MODEL),
        ),
    ]
