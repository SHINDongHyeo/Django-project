# Generated by Django 5.0.1 on 2024-02-13 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
