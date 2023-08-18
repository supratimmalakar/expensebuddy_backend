# Generated by Django 4.2.4 on 2023-08-18 07:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_user_first_name_user_is_onboarded_user_last_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buddyship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_people', to=settings.AUTH_USER_MODEL)),
                ('to_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_people', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='buddyships',
            field=models.ManyToManyField(related_name='related_to', through='authentication.Buddyship', to=settings.AUTH_USER_MODEL),
        ),
    ]
