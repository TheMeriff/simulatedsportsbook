from django.db import models


class Event(models.Model):
    NBA = 'nba'
    NFL = 'nfl'

    SPORTS = [
        (NBA, 'NBA'),
        (NFL, 'NFL'),
    ]
    external_id = models.CharField(max_length=100, null=True, blank=True)
    sport = models.CharField(choices=SPORTS, max_length=20, null=False, blank=False)
    home_team = models.CharField(max_length=75, null=True, blank=True)
    away_team = models.CharField(max_length=75, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    spread_away_team_points = models.IntegerField(blank=True, null=True)
    spread_home_team_points = models.IntegerField(blank=True, null=True)
    spread_away_team_price = models.IntegerField(blank=True, null=True)
    spread_home_team_price = models.IntegerField(blank=True, null=True)
    over_under_points = models.IntegerField(blank=True, null=True)
    over_price = models.IntegerField(blank=True, null=True)
    under_price = models.IntegerField(blank=True, null=True)
    away_team_money_line_price = models.IntegerField(blank=True, null=True)
    home_team_money_line_price = models.IntegerField(blank=True, null=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    external_sportsbook = models.CharField(max_length=75, null=True, blank=True)

    def __str__(self):
        return f'{self.sport.upper()} | {self.home_team} | {self.away_team}'
