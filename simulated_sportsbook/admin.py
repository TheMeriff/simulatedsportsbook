from django.contrib import admin

from simulated_sportsbook.models import Event, Betslip
from users.models import Account, AccountAdjustments


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = ['sport', 'home_team', 'away_team', 'start_time', 'last_updated', 'spread_away_team_points',
              'spread_away_team_price', 'spread_home_team_points', 'spread_home_team_price', 'over_under_points',
              'over_price', 'under_price', 'away_team_money_line_price', 'home_team_money_line_price',
              'external_sportsbook', 'away_team_points_scored', 'home_team_points_scored', 'completed'
              ]
    list_display = [
        'id', 'sport', 'home_team', 'away_team', 'start_time', 'over_under_points', 'spread_away_team_points',
        'spread_away_team_price', 'spread_home_team_points', 'spread_home_team_price', 'external_sportsbook',
        'away_team_money_line_price', 'home_team_money_line_price', 'last_updated', 'away_team_points_scored',
        'home_team_points_scored', 'completed'
    ]
    list_filter = ['sport', 'start_time', 'external_sportsbook', 'completed']
    ordering = ['sport', 'home_team', 'away_team', 'away_team_points_scored', 'home_team_points_scored']
    search_fields = ['home_team', 'away_team']
    filter_horizontal = ()
    fieldsets = ()


@admin.register(Betslip)
class BetslipAdmin(admin.ModelAdmin):
    fields = ['user_account', 'type_of_bet', 'predicted_outcome', 'event', 'stake', 'total_return', 'profit',
              'winning_ticket', 'processed_ticket']
    readonly_fields = ['user_account', 'type_of_bet', 'predicted_outcome', 'event', 'stake', 'total_return', 'profit',
              'winning_ticket', 'processed_ticket']
    list_display = ['user_account', 'type_of_bet', 'predicted_outcome', 'event', 'stake', 'total_return', 'profit',
                    'winning_ticket', 'processed_ticket']
    ordering = ['user_account', 'event', 'stake', 'total_return', 'profit', 'winning_ticket']
    search_fields = ['user_account', 'event']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    fields = ['user', 'current_balance', 'starting_balance']
    readonly_fields = ['user', 'current_balance']
    list_display = ['id', 'user', 'current_balance']
    list_filter = ['user', 'current_balance']
    ordering = []
    search_fields = ['user', 'current_balance']
    fieldsets = []


@admin.register(AccountAdjustments)
class AccountAdjustmentsAdmin(admin.ModelAdmin):
    fields = ['user_account', 'previous_balance', 'new_balance', 'amount_adjusted', 'notes']
    readonly_fields = ['user_account', 'previous_balance', 'new_balance', 'amount_adjusted']
    list_filter = []
    ordering = []
    search_fields = ['user_account']
    fieldsets = []

