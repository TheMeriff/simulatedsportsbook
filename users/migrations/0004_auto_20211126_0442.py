# Generated by Django 3.2.9 on 2021-11-26 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_account_account_resets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='current_balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=1000.0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='starting_balance',
            field=models.DecimalField(decimal_places=2, default=1000.0, max_digits=10),
        ),
    ]