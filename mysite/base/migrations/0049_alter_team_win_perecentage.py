# Generated by Django 4.2.5 on 2023-10-04 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0048_remove_team_games_played_remove_team_games_won_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='win_perecentage',
            field=models.FloatField(default=0),
        ),
    ]
