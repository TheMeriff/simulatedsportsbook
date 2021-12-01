from django.db import models

from users.models import Account


class Event(models.Model):
    NBA = 'nba'
    NFL = 'nfl'
    MMA = 'mma'
    CUSTOM = 'custom'
    NHL = 'nhl'
    NCAAB = 'ncaab'

    SPORTS = [
        (NBA, 'NBA'),
        (NFL, 'NFL'),
        (MMA, 'MMA'),
        (CUSTOM, 'CUSTOM'),
        (NHL, 'NHL'),
        (NCAAB, 'NCAAB')
    ]

    external_id = models.CharField(max_length=100, null=True, blank=True)
    sport = models.CharField(choices=SPORTS, max_length=20, null=False, blank=False)
    home_team = models.CharField(max_length=75, null=True, blank=True)
    away_team = models.CharField(max_length=75, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    spread_away_team_points = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    spread_home_team_points = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    spread_away_team_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    spread_home_team_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    over_under_points = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    over_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    under_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    away_team_money_line_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    home_team_money_line_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    last_updated = models.DateTimeField(null=True, blank=True)
    external_sportsbook = models.CharField(max_length=75, null=True, blank=True)
    completed = models.BooleanField(default=False)
    away_team_points_scored = models.IntegerField(null=True, blank=True)
    home_team_points_scored = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.away_team} at {self.home_team} | {self.start_time.month}/{self.start_time.day}/{self.start_time.year} @ ' \
               f'{self.start_time.hour}:{self.start_time.minute}'


class Betslip(models.Model):
    MONEY_LINE = 'money line'
    SPREAD = 'spread'
    OVER_UNDER = 'over under'

    TYPES = [
        (MONEY_LINE, 'Money Line'),
        (SPREAD, 'Spread'),
        (OVER_UNDER, 'Over Under')
    ]

    user_account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name='account')
    type_of_bet = models.CharField(choices=TYPES, max_length=20, null=False, blank=False, default=MONEY_LINE)
    predicted_outcome = models.CharField(max_length=75, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name='selected_event')
    stake = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_return = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    winning_ticket = models.BooleanField(default=False)
    processed_ticket = models.BooleanField(default=False)

    def __str__(self):
        return f'id: {self.id} | {self.type_of_bet} | {self.predicted_outcome} | Stake: {self.stake}'
