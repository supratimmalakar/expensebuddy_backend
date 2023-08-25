# Generated by Django 4.2.4 on 2023-08-24 20:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_buddy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buddy',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='buddies', to=settings.AUTH_USER_MODEL),
        ),
    ]