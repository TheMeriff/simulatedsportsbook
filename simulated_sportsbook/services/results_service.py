import time
from datetime import datetime, timedelta

import requests
from sportsreference.nfl.boxscore import Boxscore
from sportsreference.ncaab.boxscore import Boxscore as ncaaboxscore
from sportsreference.ncaab.teams import Teams
from sportsreference.nhl.boxscore import Boxscore as nhlboxscore

from simulated_sportsbook.models import Event
from simulated_sportsbook.services.discord_service import DiscordService
from simulated_sportsbook.tests.fixtures.nba_fixture import nba_team_abbreviations
from simulated_sportsbook.tests.fixtures.ncaab_fixture import ncaab_team_abbreviations
from simulated_sportsbook.tests.fixtures.nfl_fixture import nfl_team_abbreviations
from simulated_sportsbook.tests.fixtures.nhl_fixture import nhl_team_abbreviations


class ResultsService:
    def __init__(self):
        pass

    @staticmethod
    def process_nfl_events():
        updated_events = []
        nfl_events = Event.objects.filter(sport=Event.NFL).exclude(completed=True)
        if nfl_events:
            for event in nfl_events:
                updated_event = ResultsService.get_nfl_result(event)
                updated_events.append(updated_event)
                print(f'Updated {len(updated_events)} NFL events with scores and marked them as complete.')
        else:
            print('No NFL events to update')

    @staticmethod
    def get_nfl_result(event):
        team_abbreviation = nfl_team_abbreviations[event.home_team]
        if event.start_time.day < 10:
            day = f'0{event.start_time.day}'
        else:
            day = event.start_time.day
        url = f'{event.start_time.year}{event.start_time.month}{day}0{team_abbreviation.lower()}'
        boxscore = Boxscore(url)
        # Check both in the event of one team getting shutout
        if boxscore.home_points or boxscore.away_points:
            event.away_team_points_scored = boxscore.away_points
            event.home_team_points_scored = boxscore.home_points
            event.last_updated = datetime.utcnow()
            event.completed = True
            event.save()
            print(f'{event} was successfully updated with a score.')
            if event.away_team_points_scored > event.home_team_points_scored:
                winning_team = event.away_team
                higher_num = event.away_team_points_scored
                lower_num = event.home_team_points_scored
            elif event.home_team_points_scored > event.away_team_points_scored:
                winning_team = event.home_team
                higher_num = event.home_team_points_scored
                lower_num = event.away_team_points_scored
            else:
                winning_team = 'Shit broke got a problem yo.'
                higher_num = 'Shit broke got a problem yo.'
                lower_num = 'Shit broke got a problem yo.'
            score_data = f"{event.away_team} at {event.home_team}"
            DiscordService().post_score(score_data, '918755041794478110')
            time.sleep(1)
            score_data_2 = f"Winner: {winning_team}"
            DiscordService().post_score(score_data_2, '918755041794478110')
            time.sleep(1)
            score_data_3 = f"{higher_num} - {lower_num}"
            DiscordService().post_score(score_data_3, '918755041794478110')
            time.sleep(1)
            score_data_4 = '--------------------------------------'
            DiscordService().post_score(score_data_4, '918755041794478110')
        return event

    @staticmethod
    def process_nba_events():
        updated_events = []
        now = datetime.utcnow()
        date_filter = now - timedelta(hours=5)
        nba_events = Event.objects.filter(sport=Event.NBA).exclude(start_time__gte=date_filter).exclude(completed=True)
        if nba_events:
            for event in nba_events:
                updated_event = ResultsService.get_nba_result(event)
                updated_events.append(updated_event)
                print(f'Updated {len(updated_events)} NBA events with scores and marked them as complete.')
        else:
            print('No NBA games to update')

    @staticmethod
    def get_nba_result(event):
        away_team_abbreviation = nba_team_abbreviations[event.away_team]
        home_team_abbreviation = nba_team_abbreviations[event.home_team]

        if event.start_time.day < 10:
            day = f'0{event.start_time.day}'
        else:
            day = event.start_time.day

        date_for_url = f'{event.start_time.year}{event.start_time.month}{day}'
        r = requests.get(f'http://data.nba.net/10s/prod/v1/{date_for_url}/scoreboard.json')
        if r.status_code == 200:
            data = r.json()
            games = data['games']
            for game in games:
                if game['vTeam']['triCode'] == away_team_abbreviation and game['hTeam']['triCode'] == home_team_abbreviation:
                    if game['hTeam']['score'] != '' and game['vTeam']['score'] != '':
                        event.home_team_points_scored = game['hTeam']['score']
                        event.away_team_points_scored = game['vTeam']['score']
                        event.completed = True
                        event.save()
                        print(f'{event} was successfully updated with a score.')
                        if int(event.away_team_points_scored) > int(event.home_team_points_scored):
                            winning_team = event.away_team
                            higher_num = event.away_team_points_scored
                            lower_num = event.home_team_points_scored
                        elif int(event.home_team_points_scored) > int(event.away_team_points_scored):
                            winning_team = event.home_team
                            higher_num = event.home_team_points_scored
                            lower_num = event.away_team_points_scored
                        else:
                            winning_team = 'Shit broke got a problem yo.'
                            higher_num = 'Shit broke got a problem yo.'
                            lower_num = 'Shit broke got a problem yo.'
                        score_data = f"{event.away_team} at {event.home_team}"
                        DiscordService().post_score(score_data, '918755540736307221')
                        time.sleep(1)
                        score_data_2 = f"Winner: {winning_team}"
                        DiscordService().post_score(score_data_2, '918755540736307221')
                        time.sleep(1)
                        score_data_3 = f"{higher_num} - {lower_num}"
                        DiscordService().post_score(score_data_3, '918755540736307221')
                        time.sleep(1)
                        score_data_4 = '--------------------------------------'
                        DiscordService().post_score(score_data_4, '918755540736307221')

                    return event
        else:
            raise Exception

    @staticmethod
    def process_nhl_events():
        updated_events = []
        nhl_events = Event.objects.filter(sport=Event.NHL).exclude(completed=True)
        if nhl_events:
            for event in nhl_events:
                updated_event = ResultsService.get_nhl_result(event)
                updated_events.append(updated_event)
            if len(updated_events) > 0:
                print(f'Updated {len(updated_events)} NHL events with scores and marked them as complete.')
        else:
            print('No NHL events to update')

    @staticmethod
    def get_nhl_result(event):
        team_abbreviation = nhl_team_abbreviations[event.home_team]
        if event.start_time.day < 10:
            day = f'0{event.start_time.day}'
        else:
            day = event.start_time.day
        url = f'{event.start_time.year}{event.start_time.month}{day}0{team_abbreviation.upper()}'
        boxscore = nhlboxscore(url)
        # Check both in the event one team is shutout
        if boxscore.home_goals or boxscore.away_goals:
            event.away_team_points_scored = boxscore.away_goals
            event.home_team_points_scored = boxscore.home_goals
            event.last_updated = datetime.utcnow()
            event.completed = True
            event.save()
            print(f'{event} was successfully updated with a score.')
            if boxscore.home_goals == boxscore.away_goals:
                # determine who won the shoot out
                winning_team = boxscore.winning_name
                if event.home_team == winning_team:
                    event.home_team_points_scored += 1
                    event.save()
                elif event.away_team == winning_team:
                    event.away_team_points_scored += 1
                    event.save()

            if event.away_team_points_scored > event.home_team_points_scored:
                winning_team = event.away_team
                higher_num = event.away_team_points_scored
                lower_num = event.home_team_points_scored
            elif event.home_team_points_scored > event.away_team_points_scored:
                winning_team = event.home_team
                higher_num = event.home_team_points_scored
                lower_num = event.away_team_points_scored
            else:
                winning_team = 'Shit broke got a problem yo.'
                higher_num = 'Shit broke got a problem yo.'
                lower_num = 'Shit broke got a problem yo.'
            score_data = f"{event.away_team} at {event.home_team}"
            DiscordService().post_score(score_data, '918756459368566784')
            time.sleep(1)
            score_data2 = f"Winner : {winning_team}"
            DiscordService().post_score(score_data2, '918756459368566784')
            time.sleep(1)
            score_data3 = f"{higher_num} - {lower_num}"
            DiscordService().post_score(score_data3, '918756459368566784')
            score_data_4 = '--------------------------------------'
            DiscordService().post_score(score_data_4, '918756459368566784')

        return event

    @staticmethod
    def process_ncaab_events():
        updated_events = []
        now = datetime.utcnow()
        ncaab_events = Event.objects.filter(sport=Event.NCAAB).exclude(completed=True)
        if ncaab_events:
            for event in ncaab_events:
                updated_event = ResultsService.get_ncaab_result(event)
                updated_events.append(updated_event)
            if len(updated_events) > 0:
                print(f'Updated {len(updated_events)} NHL events with scores and marked them as complete.')
        else:
            print('No NCAAB events to update')

    @staticmethod
    def get_ncaab_result(event):
        url = f'{event.start_time.year}-{event.start_time.month}-{event.start_time.day}-{event.home_team.replace(" ", "-").lower()}'
        boxscore = ncaaboxscore(url)
        # Check both in the event one team is shutout
        if boxscore.home_points or boxscore.away_points:
            event.away_team_points_scored = boxscore.away_points
            event.home_team_points_scored = boxscore.home_points
            event.last_updated = datetime.utcnow()
            event.completed = True
            event.save()
            print(f'{event} was successfully updated with a score.')

        return event
