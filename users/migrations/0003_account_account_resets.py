# Generated by Django 3.2.9 on 2021-11-25 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20211121_0205'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_resets',
            field=models.IntegerField(default=0),
        ),
    ]
