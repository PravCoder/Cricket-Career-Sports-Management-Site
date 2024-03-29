# Generated by Django 3.2.8 on 2022-07-12 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_team_games'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='team1_batting_score',
            new_name='batting_score1',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='team1_bowling_score',
            new_name='batting_score2',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='team2_batting_score',
            new_name='bowling_score1',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='team2_bowling_score',
            new_name='bowling_score2',
        ),
    ]
