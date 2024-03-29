# Generated by Django 4.0.5 on 2023-09-02 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0027_remove_playergamestat_wicket_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='current_bowler',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_bowler', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='off_strike_batsman',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='off_strike_batsman', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game',
            name='on_strike_batsman',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='on_strike_batsman', to=settings.AUTH_USER_MODEL),
        ),
    ]
