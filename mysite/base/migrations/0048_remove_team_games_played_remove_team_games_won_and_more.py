# Generated by Django 4.2.5 on 2023-10-04 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0047_team_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='games_played',
        ),
        migrations.RemoveField(
            model_name='team',
            name='games_won',
        ),
        migrations.AddField(
            model_name='team',
            name='win_perecentage',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
