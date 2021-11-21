from datetime import datetime, timedelta

import requests
from sportsreference.nfl.boxscore import Boxscore

from simulated_sportsbook.models import Event
from simulated_sportsbook.tests.fixtures.nba_fixture import nba_team_abbreviations
from simulated_sportsbook.tests.fixtures.nfl_fixture import nfl_team_abbreviations


class ResultsService:
    def __init__(self):
        pass

    @staticmethod
    def process_nfl_events():
        updated_events = []
        now = datetime.utcnow()
        date_filter = now - timedelta(hours=16)
        nba_events = Event.objects.filter(sport=Event.NFL).exclude(start_time__gte=date_filter).exclude(completed=True)
        for event in nba_events:
            updated_event = ResultsService.get_nfl_result(event)
            updated_events.append(updated_event)
        print(f'Updated {len(updated_events)} NBA events with scores and marked them as complete.')

    @staticmethod
    def get_nfl_result(event):
        team_abbreviation = nfl_team_abbreviations[event.home_team]
        url = f'{event.start_time.year}{event.start_time.month}{event.start_time.day}0{team_abbreviation.lower()}'
        boxscore = Boxscore(url)
        event.away_team_points_scored = boxscore.away_points
        event.home_team_points_scored = boxscore.home_points
        event.last_updated = datetime.utcnow()
        event.save()

        return event

    @staticmethod
    def process_nba_events():
        updated_events = []
        now = datetime.utcnow()
        date_filter = now - timedelta(hours=10)
        nba_events = Event.objects.filter(sport=Event.NBA).exclude(start_time__gte=date_filter).exclude(completed=True)
        for event in nba_events:
            updated_event = ResultsService.get_nba_result(event)
            updated_events.append(updated_event)
        print(f'Updated {len(updated_events)} NBA events with scores and marked them as complete.')

    @staticmethod
    def get_nba_result(event):
        away_team_abbreviation = nba_team_abbreviations[event.away_team]
        home_team_abbreviation = nba_team_abbreviations[event.home_team]

        date_for_url = f'{event.start_time.year}{event.start_time.month}{event.start_time.day}'
        r = requests.get(f'http://data.nba.net/10s/prod/v1/{date_for_url}/scoreboard.json')
        if r.status_code == 200:
            data = r.json()
            games = data['games']
            for game in games:
                if game['vTeam']['triCode'] == away_team_abbreviation and game['hTeam']['triCode'] == home_team_abbreviation:
                    event.home_team_points_scored = game['hTeam']['score']
                    event.away_team_points_scored = game['vTeam']['score']
                    event.completed = True
                    event.save()
                    print(f'{event} was successfully updated with a score.')

                    return event
        else:
            raise Exception
