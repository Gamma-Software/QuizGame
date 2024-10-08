# Generated by Django 5.1.2 on 2024-10-08 23:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0007_player_current_session"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="order",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="player",
            name="current_session",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.quizsession",
            ),
        ),
    ]
