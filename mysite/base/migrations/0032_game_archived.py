# Generated by Django 4.2.5 on 2023-09-15 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_rename_completed_game_entering_stats'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='archived',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
