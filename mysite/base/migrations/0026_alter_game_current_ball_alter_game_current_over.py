# Generated by Django 4.0.5 on 2023-09-01 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_alter_game_current_innings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='current_ball',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='current_over',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
