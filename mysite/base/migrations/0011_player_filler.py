# Generated by Django 3.2.8 on 2022-07-02 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20220701_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='filler',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
