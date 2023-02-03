import time
from datetime import datetime, timedelta

import requests
from sportsreference.nfl.boxscore import Boxscore, Boxscores
from sportsreference.ncaab.boxscore import Boxscore as ncaaboxscore
from sportsreference.mlb.boxscore import Boxscore as mlbboxscore
from sportsreference.nhl.boxscore import Boxscore as nhlboxscore

from simulated_sportsbook.models import Event
from simulated_sportsbook.services.discord_service import DiscordService
from simulated_sportsbook.tests.fixtures.mlb_fixture import mlb_team_abbreviations
from simulated_sportsbook.tests.fixtures.nba_fixture import nba_team_abbreviations
from simulated_sportsbook.tests.fixtures.nhl_fixture import nhl_team_abbreviations


class ResultsService:
    def __init__(self):
        self.session = requests.session()
        possible_api_keys = []
        self.session.headers.update({'X-RapidAPI-Key': possible_api_keys[1]})

    @staticmethod
    def process_nfl_events():
        week = None
        updated_events = []
        completed_nfl_events = Event.objects.filter(sport=Event.NFL).exclude(completed=True)
        event_map = {f'{event.away_team} @ {event.home_team}': event for event in completed_nfl_events}
        nfl_weeks = {
            # September
            '9': {
                '1': range(8, 13),
                '2': range(14, 20),
                '3': range(21, 27),
                '4': range(28, 30),
            },
            # October
            '10': {
                '4': range(1, 5),
                '5': range(5, 12),
                '6': range(12, 19),
                '7': range(19, 26),
                '8': range(26, 32),
            },
            # November
            '11': {
                '8': 1,
                '9': range(2, 9),
                '10': range(9, 16),
                '11': range(16, 23),
                '12': range(23, 30),
                '13': 30,
            },
            # December
            '12': {
                '13': range(1, 7),
                '14': range(7, 14),
                '15': range(14, 21),
                '16': range(21, 28),
                '17': range(28, 31),
            },
            # January
            '1': {
                '17': range(1, 4),
                '18': range(4, 12),
            },
        }

        # Only run logic if we have events to process
        if completed_nfl_events:
            # Get the current datetime
            utc_now = datetime.utcnow()
            offset = timedelta(hours=6)
            now = utc_now - offset
            # Narrow down the weeks to check by month
            weeks_to_check = nfl_weeks[str(now.month)]
            # Find the correct nfl week
            for week, days in weeks_to_check.items():
                print(f'Days in this NFL week {[day for day in days]}')
                if now.day in days:
                    print(f'Today: {now.month}/{now.day}/{now.year} is week {week} of the nfl season')
                    break

            # Make a request for that weeks boxscores
            if week:
                try:
                    boxscores = Boxscores(week=int(week), year=2022)
                    game_results = boxscores.games[f'{week}-{now.year}']
                    result_map = {f'{game["away_name"]} @ {game["home_name"]}': game for game in game_results}
                    for matchup, data in result_map.items():
                        event = event_map.get(matchup, None)
                        if event and all([data.get('home_score', None), data.get('away_score', None)]):
                            event.away_team_points_scored = data['away_score']
                            event.home_team_points_scored = data['home_score']
                            event.completed = True
                            updated_events.append(event)
                            print(f'{event} was successfully updated with a score.')
                except Exception as e:
                    print(e)

        if updated_events:
            Event.objects.bulk_update(updated_events, fields=('home_team_points_scored', 'away_team_points_scored', 'completed'))
            print(f'Updated {len(updated_events)} NFL events')
        else:
            print('No NFL events to update')

    # @staticmethod
    # def get_nfl_result(event):
    #     team_abbreviation = nfl_team_abbreviations[event.home_team]
    #     if event.start_time.day < 10:
    #         day = f'0{event.start_time.day}'
    #     else:
    #         day = event.start_time.day
    #
    #     if event.start_time.month < 10:
    #         month = f'0{event.start_time.month}'
    #     else:
    #         month = event.start_time.month
    #
    #     url = f'{event.start_time.year}{month}{day}0{team_abbreviation.lower()}'
    #     boxscore = Boxscore(url)
    #     # Check both in the event of one team getting shutout
    #     if boxscore.home_points or boxscore.away_points:
    #         event.away_team_points_scored = boxscore.away_points
    #         event.home_team_points_scored = boxscore.home_points
    #         event.last_updated = datetime.utcnow()
    #         event.completed = True
    #         event.save()
    #         print(f'{event} was successfully updated with a score.')
    #         if event.away_team_points_scored > event.home_team_points_scored:
    #             winning_team = event.away_team
    #             higher_num = event.away_team_points_scored
    #             lower_num = event.home_team_points_scored
    #         elif event.home_team_points_scored > event.away_team_points_scored:
    #             winning_team = event.home_team
    #             higher_num = event.home_team_points_scored
    #             lower_num = event.away_team_points_scored
    #         else:
    #             winning_team = 'Shit broke got a problem yo.'
    #             higher_num = 'Shit broke got a problem yo.'
    #             lower_num = 'Shit broke got a problem yo.'
    #         score_data = f"{event.away_team} at {event.home_team}"
    #         DiscordService().post_score(score_data, '918755041794478110')
    #         time.sleep(1)
    #         score_data_2 = f"Winner: {winning_team}"
    #         DiscordService().post_score(score_data_2, '918755041794478110')
    #         time.sleep(1)
    #         score_data_3 = f"{higher_num}-{lower_num}"
    #         DiscordService().post_score(score_data_3, '918755041794478110')
    #         time.sleep(1)
    #         score_data_4 = '--------------------------------------'
    #         DiscordService().post_score(score_data_4, '918755041794478110')
    #     return event

    @staticmethod
    def process_nba_events():
        updated_events = []
        date_game_map = {}
        now = datetime.utcnow()
        date_filter = now - timedelta(hours=5)
        nba_events = Event.objects.filter(sport=Event.NBA).exclude(start_time__gte=date_filter).exclude(completed=True)
        for event in nba_events:
            if event.start_time.day < 10:
                day = f'0{event.start_time.day}'
            else:
                day = event.start_time.day

            if event.start_time.month < 10:
                month = f'0{event.start_time.month}'
            else:
                month = event.start_time.month
            formatted_date_range = f'{event.start_time.year}-{month}-{day}'
            if not date_game_map.get(formatted_date_range):
                date_game_map[formatted_date_range] = []

            date_game_map[formatted_date_range].append(event)

        if nba_events:
            updated_events = ResultsService().get_nba_results(date_game_map)
            Event.objects.bulk_update(updated_events, fields=(
                'away_team_points_scored',
                'completed',
                'home_team_points_scored',
                'last_updated'
            ))
            print(f'Updated {len(updated_events)} NBA events with scores and marked them as complete.')
        else:
            print('No NBA games to update')

    def get_nba_results(self, date_game_map):
        self.session.headers.update({'X-RapidAPI-Host': 'api-nba-v1.p.rapidapi.com'})
        updated_events = []

        try:
            for date in date_game_map.keys():
                url = f'https://api-nba-v1.p.rapidapi.com/games?date={date}'
                # For rate limit
                time.sleep(10)
                r = self.session.get(url)
                data = r.json()['response']
                print(f"\n Remaining daily requests {r.headers['x-ratelimit-requests-remaining']} \n")
                for game in data:
                    away_team = game['teams']['visitors']['name']
                    home_team = game['teams']['home']['name']
                    for event in date_game_map[date]:
                        if all((away_team == event.away_team, home_team == event.home_team)):
                            event.away_team_points_scored = game['scores']['visitors']['points']
                            event.home_team_points_scored = game['scores']['home']['points']
                            event.last_updated = datetime.utcnow()
                            event.completed = True
                            updated_events.append(event)
                            print(f'Updated {event}')
        except Exception as e:
            print(f'Error updating NBA games. | {e}')
        return updated_events

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

        if event.start_time.month < 10:
            month = f'0{event.start_time.month}'
        else:
            month = event.start_time.month

        url = f'{event.start_time.year}{month}{day}0{team_abbreviation.upper()}'
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
            score_data3 = f"{higher_num}-{lower_num}"
            DiscordService().post_score(score_data3, '918756459368566784')
            score_data_4 = '--------------------------------------'
            DiscordService().post_score(score_data_4, '918756459368566784')

        return event

    @staticmethod
    def process_mlb_events():
        updated_events = []
        mlb_events = Event.objects.filter(sport=Event.MLB).exclude(completed=True)
        if mlb_events:
            for event in mlb_events:
                updated_event = ResultsService.get_mlb_result(event)
                updated_events.append(updated_event)
            if len(updated_events) > 0:
                print(f'Updated {len(updated_events)} MLB events with scores and marked them as complete.')
        else:
            print('No MLB events to update')

    @staticmethod
    def get_mlb_result(event):
        # away_team_abbreviation = mlb_team_abbreviations[event.away_team]
        home_team_abbreviation = mlb_team_abbreviations[event.home_team]

        if event.start_time.day < 10:
            day = f'0{event.start_time.day}'
        else:
            day = event.start_time.day

        if event.start_time.month < 10:
            month = f'0{event.start_time.month}'
        else:
            month = event.start_time.month

        url = f'{home_team_abbreviation}/{home_team_abbreviation}{event.start_time.year}{month}{day}0'
        boxscore = mlbboxscore(url)
        # Check both in the event one team is shutout
        if boxscore.home_runs or boxscore.away_runs:
            event.away_team_points_scored = boxscore.away_runs
            event.home_team_points_scored = boxscore.home_runs
            event.last_updated = datetime.utcnow()
            event.completed = True
            event.save()
            print(f'{event} was successfully updated with a score.')

    @staticmethod
    def process_ncaab_events():
        updated_events = []
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
