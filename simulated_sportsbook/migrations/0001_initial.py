# Generated by Django 3.2.9 on 2021-11-20 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=100, null=True)),
                ('sport', models.CharField(choices=[('nba', 'NBA'), ('nfl', 'NFL')], max_length=20)),
                ('home_team', models.CharField(blank=True, max_length=75, null=True)),
                ('away_team', models.CharField(blank=True, max_length=75, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('spread_away_team_points', models.IntegerField(blank=True, null=True)),
                ('spread_home_team_points', models.IntegerField(blank=True, null=True)),
                ('spread_away_team_price', models.IntegerField(blank=True, null=True)),
                ('spread_home_team_price', models.IntegerField(blank=True, null=True)),
                ('over_under_points', models.IntegerField(blank=True, null=True)),
                ('over_price', models.IntegerField(blank=True, null=True)),
                ('under_price', models.IntegerField(blank=True, null=True)),
                ('away_team_money_line_price', models.IntegerField(blank=True, null=True)),
                ('home_team_money_line_price', models.IntegerField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
                ('external_sportsbook', models.CharField(blank=True, max_length=75, null=True)),
            ],
        ),
    ]
