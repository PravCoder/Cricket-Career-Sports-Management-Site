# Generated by Django 4.2.5 on 2023-09-28 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0041_game_team1_players_game_team2_players'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='temporary',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
