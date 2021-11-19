from django.contrib import admin

from simulated_sportsbook.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ['sport', 'home_team', 'away_team', 'start_time', 'spread_away_team_points', 'spread_away_team_price',
              'spread_home_team_points', 'spread_home_team_price', 'over_under',
              'away_team_money_line_price', 'home_team_money_line_price', 'last_updated']
    list_display = [
        'id', 'sport', 'home_team', 'away_team', 'start_time', 'spread_away_team_points', 'spread_away_team_price',
              'spread_home_team_points', 'spread_home_team_price', 'over_under',
              'away_team_money_line_price', 'home_team_money_line_price', 'last_updated']
    list_filter = ['sport', 'start_time', 'spread_home_team_points', 'spread_away_team_points']
    ordering = ['sport', 'home_team', 'away_team']
    search_fields = ['home_team', 'away_team']
    filter_horizontal = ()
    fieldsets = ()
