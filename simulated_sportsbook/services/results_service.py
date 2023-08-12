import time
from datetime import datetime, timedelta, timezone

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
        possible_api_keys = ['485c543b43mshda433513811d928p197761jsn1e3643bf923c']
        self.session.headers.update({'X-RapidAPI-Key': possible_api_keys[0]})

    # def process_nfl_events(self):
    #     week = None
    #     updated_events = []
    #     completed_nfl_events = Event.objects.filter(sport=Event.NFL).exclude(completed=True)
    #     event_map = {f'{event.away_team} @ {event.home_team}': event for event in completed_nfl_events}
    #     nfl_weeks = {
    #         # September
    #         '9': {
    #             '1': range(8, 13),
    #             '2': range(14, 20),
    #             '3': range(21, 27),
    #             '4': range(28, 30),
    #         },
    #         # October
    #         '10': {
    #             '4': range(1, 5),
    #             '5': range(5, 12),
    #             '6': range(12, 19),
    #             '7': range(19, 26),
    #             '8': range(26, 32),
    #         },
    #         # November
    #         '11': {
    #             '8': [1],
    #             '9': range(2, 9),
    #             '10': range(9, 16),
    #             '11': range(16, 23),
    #             '12': range(23, 30),
    #             '13': 30,
    #         },
    #         # December
    #         '12': {
    #             '13': range(1, 7),
    #             '14': range(7, 14),
    #             '15': range(14, 21),
    #             '16': range(21, 28),
    #             '17': range(28, 31),
    #         },
    #         # January
    #         '1': {
    #             '17': range(1, 4),
    #             '18': range(4, 12),
    #         },
    #     }
    #
    #     # Only run logic if we have events to process
    #     if completed_nfl_events:
    #         # Get the current datetime
    #         utc_now = datetime.utcnow()
    #         offset = timedelta(hours=6)
    #         now = utc_now - offset
    #         # Narrow down the weeks to check by month
    #         weeks_to_check = nfl_weeks['11']
    #         # Find the correct nfl week
    #         for week, days in weeks_to_check.items():
    #             print(f'Days in this NFL week {[day for day in days]}')
    #             if now.day in days:
    #                 print(f'Today: {now.month}/{now.day}/{now.year} is week {week} of the nfl season')
    #                 break
    #
    #         # Make a request for that weeks boxscores
    #         if week:
    #             try:
    #                 boxscores = Boxscores(week=int(week), year=2023)
    #                 game_results = boxscores.games[f'{week}-{now.year}']
    #                 result_map = {f'{game["away_name"]} @ {game["home_name"]}': game for game in game_results}
    #                 for matchup, data in result_map.items():
    #                     event = event_map.get(matchup, None)
    #                     if event and all([data.get('home_score', None), data.get('away_score', None)]):
    #                         event.away_team_points_scored = data['away_score']
    #                         event.home_team_points_scored = data['home_score']
    #                         event.completed = True
    #                         updated_events.append(event)
    #                         print(f'{event} was successfully updated with a score.')
    #             except Exception as e:
    #                 print(e)
    #
    #     if updated_events:
    #         Event.objects.bulk_update(updated_events, fields=('home_team_points_scored', 'away_team_points_scored', 'completed'))
    #         print(f'Updated {len(updated_events)} NFL events')
    #     else:
    #         print('No NFL events to update')

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



    # def get_nba_results(self, date_game_map):
    #     self.session.headers.update({'X-RapidAPI-Host': 'api-nba-v1.p.rapidapi.com'})
    #     updated_events = []
    #     unable_to_update = []
    #     all_result_json = []
    #
    #     try:
    #         for date, events in date_game_map.items():
    #             url = f'https://api-nba-v1.p.rapidapi.com/games?date={date}'
    #             # For rate limit
    #             r = self.session.get(url)
    #             data = r.json()['response']
    #             all_result_json.extend(data)
    #             result_data_map = {f"{result['teams']['home']['name']}": result for result in data}
    #             print(f"\n Remaining daily requests {r.headers['x-ratelimit-requests-remaining']} \n")
    #             time.sleep(6)
    #             for event in events:
    #                 if result_data_map.get(event.home_team):
    #                     result_data = result_data_map.get(event.home_team)
    #                     event.away_team_points_scored = result_data['scores']['visitors']['points']
    #                     event.home_team_points_scored = result_data['scores']['home']['points']
    #                     event.last_updated = datetime.utcnow()
    #                     event.completed = True
    #                     updated_events.append(event)
    #                     print(f'Updated {event}')
    #                 else:
    #                     print(f'Event {event} not found in response data for {date}')
    #                     unable_to_update.append(event)
    #
    #     except Exception as e:
    #         print(f'Error updating NBA games. | {e}')
    #     print(f'Total events updated: {len(updated_events)} | Total events that failed to update: {len(unable_to_update)}')
    #     return updated_events

    # @staticmethod
    # def process_nhl_events():
    #     updated_events = []
    #     nhl_events = Event.objects.filter(sport=Event.NHL).exclude(completed=True)
    #     if nhl_events:
    #         for event in nhl_events:
    #             updated_event = ResultsService.get_nhl_result(event)
    #             updated_events.append(updated_event)
    #         if len(updated_events) > 0:
    #             print(f'Updated {len(updated_events)} NHL events with scores and marked them as complete.')
    #     else:
    #         print('No NHL events to update')
    #
    # @staticmethod
    # def get_nhl_result(event):
    #     team_abbreviation = nhl_team_abbreviations[event.home_team]
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
    #     url = f'{event.start_time.year}{month}{day}0{team_abbreviation.upper()}'
    #     boxscore = nhlboxscore(url)
    #     # Check both in the event one team is shutout
    #     if boxscore.home_goals or boxscore.away_goals:
    #         event.away_team_points_scored = boxscore.away_goals
    #         event.home_team_points_scored = boxscore.home_goals
    #         event.last_updated = datetime.utcnow()
    #         event.completed = True
    #         event.save()
    #         print(f'{event} was successfully updated with a score.')
    #         if boxscore.home_goals == boxscore.away_goals:
    #             # determine who won the shoot out
    #             winning_team = boxscore.winning_name
    #             if event.home_team == winning_team:
    #                 event.home_team_points_scored += 1
    #                 event.save()
    #             elif event.away_team == winning_team:
    #                 event.away_team_points_scored += 1
    #                 event.save()
    #
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
    #         DiscordService().post_score(score_data, '918756459368566784')
    #         time.sleep(1)
    #         score_data2 = f"Winner : {winning_team}"
    #         DiscordService().post_score(score_data2, '918756459368566784')
    #         time.sleep(1)
    #         score_data3 = f"{higher_num}-{lower_num}"
    #         DiscordService().post_score(score_data3, '918756459368566784')
    #         score_data_4 = '--------------------------------------'
    #         DiscordService().post_score(score_data_4, '918756459368566784')
    #
    #     return event

    def process_mlb_events(self):
        daily_games = None
        events_to_update = []
        game_data = []

        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        yesterday = now - timedelta(days=1)
        mlb_events = Event.objects.filter(sport=Event.MLB).exclude(start_time__gte=yesterday).exclude(completed=True)
        existing_event_map = {f"{event.away_team} at {event.home_team}": event for event in mlb_events}
        event_dates = []
        unique_dates = set()
        for event in mlb_events:
            if (event.start_time.month, event.start_time.day, event.start_time.year) not in unique_dates:
                # Use the set to update unique date info
                unique_dates.add((event.start_time.month, event.start_time.day, event.start_time.year))
                # Keep the unique datetime objs in a list.
                event_dates.append(event.start_time)

        if event_dates:
            for date in event_dates:
                time.sleep(1)
                daily_games = ResultsService().get_mlb_result(date=date)
                game_data.append(daily_games)
        else:
            print('No MLB events to update')

        # Update games
        if daily_games:
            for games in daily_games:
                game = games['game']
                home_team = f"{game['home']['market']} {game['home']['name']}"
                away_team = f"{game['away']['market']} {game['away']['name']}"
                home_score = game['home']['runs']
                away_score = game['away']['runs']
                game_time = datetime.strptime(game['scheduled'], '%Y-%m-%dT%H:%M:%S%z')
                formatted_game_key = f"{away_team} at {home_team}"
                matched_event = existing_event_map.get(formatted_game_key)
                if matched_event and game_time <= yesterday:
                    matched_event.home_team_points_scored = home_score
                    matched_event.away_team_points_scored = away_score
                    matched_event.completed = True
                    events_to_update.append(matched_event)
                    print(f'Matched {formatted_game_key} with {matched_event} event map')

            if events_to_update:
                Event.objects.bulk_update(events_to_update, fields=('home_team_points_scored', 'away_team_points_scored', 'completed'), batch_size=200)
                print(f"Updated {len(events_to_update)} MLB games")

    def format_month_date(self, date):
        # Format dates for url
        if date.day < 10:
            day = f'0{date.day}'
        else:
            day = date.day

        if date.month < 10:
            month = f'0{date.month}'
        else:
            month = date.month

        return month, day

    def get_mlb_result(self, date):
        # Replace with your actual SportsRadar API key
        api_key = "xaq54mf8mngfz92pbk53w8hm"

        month, day = self.format_month_date(date)

        # URL for the MLB scores endpoint
        url = f"https://api.sportradar.com/mlb/trial/v7/en/games/{date.year}/{month}/{day}/boxscore.json?api_key={api_key}"

        try:
            # Make the GET request
            response = requests.get(url)
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                games = data['league']['games']
                return games if games else None
                # Process the data as needed
            else:
                print("Request failed with status code:", response.status_code)
        except Exception as e:
            raise e

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
