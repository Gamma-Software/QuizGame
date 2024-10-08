# Generated by Django 5.1.2 on 2024-10-08 21:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quizsession",
            name="player",
        ),
        migrations.AddField(
            model_name="quizsession",
            name="players",
            field=models.ManyToManyField(
                related_name="quiz_sessions", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
