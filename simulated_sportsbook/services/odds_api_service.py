from datetime import datetime, timedelta
from decimal import Decimal

import requests
from dateutil import parser
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
        nfl_events = []
        r = requests.get('https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?apiKey=ead60e7fddf8d0aa97a31bfdee54b5c1&regions=us&markets=h2h,spreads,totals&oddsFormat=american')
        if r.status_code == 200:
            print('Remaining requests', r.headers['x-requests-remaining'])
            print('Used requests', r.headers['x-requests-used'])
            event_records = r.json()
            for event in event_records:
                external_event_id = event['id']
                if external_event_id not in self.existing_event_map:
                    game = self.create_event(event, sport=Event.NFL)
                    nfl_events.append(game)
            return nfl_events
        else:
            print(f"{r.status_code} | {r.reason}")

    def get_nba_odds(self):
        nba_events = []
        r = requests.get('https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey=ead60e7fddf8d0aa97a31bfdee54b5c1&regions=us&markets=h2h,spreads,totals&oddsFormat=american')

        if r.status_code == 200:
            print('Remaining requests', r.headers['x-requests-remaining'])
            print('Used requests', r.headers['x-requests-used'])
            event_records = r.json()
            for event in event_records:
                external_event_id = event['id']
                if external_event_id not in self.existing_event_map:
                    game = self.create_event(event, sport=Event.NBA)
                    nba_events.append(game)
            return nba_events
        else:
            print(f"{r.status_code} | {r.reason}")

    def create_event(self, event, sport):
        money_line = None
        over_under = None
        over_points = None
        under_points = None
        over_price = None
        under_price = None
        over_under_points = None
        external_sportsbook = None
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
        start_time_obj = parser.parse(start_time)
        event_start_time = start_time_obj - timedelta(hours=6)
        home_team = event['home_team']
        away_team = event['away_team']
        bookmakers = event['bookmakers']
        for book in bookmakers:
            if book['key'] == 'fanduel':
                external_sportsbook = book['title']
                external_book_data = book
            elif book['key'] == 'draftkings':
                external_sportsbook = book['title']
                external_book_data = book
            elif book['key'] == 'unibet':
                external_sportsbook = book['title']
                external_book_data = book
            elif book['key'] == 'foxbet':
                external_sportsbook = book['title']
                external_book_data = book
            elif book['key'] == 'barstool':
                external_sportsbook = book['title']
                external_book_data = book

        if external_book_data:
            markets = external_book_data['markets']
            last_updated = external_book_data['last_update']
            last_updated_obj = parser.parse(last_updated)
            event_last_updated = last_updated_obj - timedelta(hours=6)
        if markets:
            for market in markets:
                if market['key'] == 'h2h':
                    money_line = market['outcomes']
                elif market['key'] == 'spreads':
                    spread = market['outcomes']
                elif market['key'] == 'totals':
                    over_under = market['outcomes']

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

        if over_under:
            for i in over_under:
                if i['name'] == 'Over':
                    over_points = Decimal(i['point'])
                    over_price = Decimal(i['price'])
                elif i['name'] == 'Under':
                    under_points = Decimal(i['point'])
                    under_price = Decimal(i['price'])
            if over_points == under_points:
                over_under_points = over_points

        event = Event.objects.create(
            external_id=external_event_id,
            sport=sport,
            home_team=home_team,
            away_team=away_team,
            start_time=event_start_time,
            over_price=over_price,
            under_price=under_price,
            over_under_points=over_under_points,
            spread_away_team_points=spread_away_team_points,
            spread_away_team_price=spread_away_team_price,
            spread_home_team_price=spread_home_team_price,
            spread_home_team_points=spread_home_team_points,
            away_team_money_line_price=away_team_money_line_price,
            home_team_money_line_price=home_team_money_line_price,
            last_updated=event_last_updated,
            external_sportsbook=external_sportsbook
        )
        print(f'{event.sport.upper()} Event {event.external_id} was added to database')

        return event
