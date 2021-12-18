from rest_framework import serializers

from simulated_sportsbook.models import Event


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'external_id',
            'sport',
            'external_sportsbook',
            'start_time',
            'last_updated',
            'home_team',
            'home_team_money_line_price',
            'spread_home_team_points',
            'spread_home_team_price',
            'away_team',
            'away_team_money_line_price',
            'spread_away_team_points',
            'spread_away_team_price',
            'over_under_points',
            'over_price',
            'under_price',
            'completed',
            'away_team_points_scored',
            'home_team_points_scored'
        ]