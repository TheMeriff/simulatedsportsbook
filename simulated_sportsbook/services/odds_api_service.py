from decimal import Decimal

import requests
from dateutil.tz import tz
from django.http import HttpResponse

from simulated_sportsbook.models import Event


class OpenApiService:
    def __init__(self):
        existing_events = Event.objects.all()
        self.existing_event_map = {}
        for event in existing_events:
            self.existing_event_map[event.external_id] = event

    def get_nfl_odds(self):
        r = requests.get('https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey=ead60e7fddf8d0aa97a31bfdee54b5c1&regions=us&markets=h2h,spreads&oddsFormat=american')
        if r.status_code == 200:
            event_records = r.json()
            for event in event_records:
                external_event_id = event['id']
                if external_event_id not in self.existing_event_map:
                    self.create_event(event, sport=Event.NFL)
        else:
            print(f"{r.status_code} | {r.reason}")

    def get_nba_odds(self):
        r = requests.get('https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey=ead60e7fddf8d0aa97a31bfdee54b5c1&regions=us&markets=h2h,spreads&oddsFormat=american')

        if r.status_code == 200:
            event_records = r.json()
            for event in event_records:
                external_event_id = event['id']
                if external_event_id not in self.existing_event_map:
                    self.create_event(event, sport=Event.NBA)
        else:
            print(f"{r.status_code} | {r.reason}")

    def create_event(self, event, sport):
        money_line = None
        spread_home_team_price = None
        spread_home_team_points = None
        spread_away_team_points = None
        spread_away_team_price = None
        away_team_money_line_price = None
        home_team_money_line_price = None
        spread = None
        markets = None
        external_book_data = None
        external_event_id = event['id']
        start_time = event['commence_time']
        home_team = event['home_team']
        away_team = event['away_team']
        bookmakers = event['bookmakers']
        for book in bookmakers:
            if book['key'] == 'fanduel':
                external_book_data = book
            elif book['key'] == 'draftkings':
                external_book_data = book
            elif book['key'] == 'unibet':
                external_book_data = book
            elif book['key'] == 'foxbet':
                external_book_data = book
            elif book['key'] == 'barstool':
                external_book_data = book
        if external_book_data:
            markets = external_book_data['markets']
        if markets:
            for market in markets:
                if market['key'] == 'h2h':
                    money_line = market['outcomes']
                elif market['key'] == 'spreads':
                    spread = market['outcomes']

        if spread:
            for team in spread:
                if team['name'] == home_team:
                    spread_home_team_points = Decimal(team['point'])
                    spread_home_team_price = Decimal(team['price'])
                elif team['name'] == away_team:
                    spread_away_team_points = Decimal(team['point'])
                    spread_away_team_price = Decimal(team['price'])

        if money_line:
            for team in money_line:
                if team['name'] == home_team:
                    home_team_money_line_price = Decimal(team['price'])
                if team['name'] == away_team:
                    away_team_money_line_price = Decimal(team['price'])

        event = Event.objects.create(
            external_id=external_event_id,
            sport=sport,
            home_team=home_team,
            away_team=away_team,
            start_time=start_time,
            spread_away_team_points=spread_away_team_points,
            spread_away_team_price=spread_away_team_price,
            spread_home_team_price=spread_home_team_price,
            spread_home_team_points=spread_home_team_points,
            away_team_money_line_price=away_team_money_line_price,
            home_team_money_line_price=home_team_money_line_price,
            last_updated=external_book_data['last_update'] if external_book_data else None,
        )
        print(f'{event.sport.upper()} Event {event.external_id} was added to database')

        return event
