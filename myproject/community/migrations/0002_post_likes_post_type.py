# Generated by Django 5.0.1 on 2024-02-17 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.IntegerField(default=0),
        ),
    ]
